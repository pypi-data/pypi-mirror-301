import pygame
from omegaconf import DictConfig, OmegaConf

from pymasep.common import Game
from pymasep.engine.environment_engine import EnvironmentEngine
from pymasep.engine.external_controller import ExternalController
from pymasep.communication import Message, Server, SocketHandlerQueue
from pymasep.application import SubApp, ConnectedSubAppInfo
from pymasep.logger import Logger


class Engine(SubApp):
    """
    Sub application that manages the main environment
    """

    def __init__(self, app,
                 received_q_id: int,
                 cfg: DictConfig,
                 max_connection: int = -1,
                 ) -> None:
        """
        :param app: main application
        :param received_q_id: id of the queue used by the engine to receive messages.
        :param cfg: configuration of the engine
        :param max_connection: max number of TCP connection to the engine. -1 means no possible remote communication.
        """
        super().__init__(app=app, received_q_id=received_q_id, cfg=cfg)

        self.environment = EnvironmentEngine(id_env=self.id, cfg=self.config)
        """ environment engine """

        self.old_step = None
        """ keep last step of the environment. TODO Maybe deprecated """

        self.end_game = False
        """ is the game is finished? (all episodes)"""
        if max_connection != -1:
            self.port = OmegaConf.select(self.config, 'engine.server.port')
            """ port of the server"""
            if self.port is None:
                self.port = 60000
            self.remote_communication = Server(ident=self.id,
                                               host='',
                                               port=self.port,
                                               max_connection=max_connection,
                                               socket_handler_class=SocketHandlerQueue,
                                               socket_handler_args=(self.messages_received,),
                                               wait_announcement=True)

            self.remote_communication.wait_announcement()
            self.remote_communication.wait_connection()

        self.env_logger = Logger()
        """ logger of the environment of the engine"""

        self.eps = OmegaConf.select(self.config, 'engine.eps')
        """ Expected engine loop per second"""
        if self.eps is None:
            self.eps = 100

    def set_engine_for_external_controller(self) -> None:
        """ set the engine of all external controllers during registering"""
        for ag in self.environment.agents:
            if isinstance(ag.controller, ExternalController):
                ag.controller.engine = self

    def define(self) -> None:
        """
        Wait for the "Define" message and initialize the engine according to message parameters (game, ...)
        """
        msg = self.wait_message([Message.MESSAGE_TYPE_DEFINE])
        self.environment.game = msg.params['game'](cfg=self.config)
        self.logger.debug('Define game received %s', msg.params['game'].__name__)
        self.current_event = None

    def register(self, msg_register) -> None:
        """
        Register an interface to the engine.
        For role "ACTOR", create the external agent, and configure its external controller

        :param msg_register: Message containing all interface parameters (id, role)
        """
        self.logger.debug('Register interface (id: %s role: %s)',msg_register.params['id'], msg_register.params['role'])
        if self.remote_communication is not None and \
                self.remote_communication.is_connection_registered(msg_register.params['id']):
            self.register_connected_sub_app(sub_app_id=msg_register.params['id'],
                                            role=msg_register.params['role'],
                                            sent_q=None)
        else:
            self.register_connected_sub_app(sub_app_id=msg_register.params['id'],
                                            role=msg_register.params['role'],
                                            sent_q=self.app.queues[msg_register.params['queue_id']])
        external_agent = None
        if self.connected_sub_app[msg_register.params['id']].role == ConnectedSubAppInfo.ROLE_ACTOR:
            external_agent = self.environment.game.create_external_agent(self.environment, msg_register.params['id'])
            self.environment.current_state.add_object(external_agent)
            self.connected_sub_app[msg_register.params['id']].agent_fname = external_agent.get_fullname()

        self.set_engine_for_external_controller()
        if external_agent is not None:
            self.logger.debug('New external agent %s', external_agent.get_fullname())
        self.logger.debug('Order of agents: %s, Head of order : %s ',
                         self.environment.game.get_system_value(self.environment.current_state, 'AgentOrder'),
                         self.environment.game.get_system_value(self.environment.current_state, 'AgentOrder').head)

    def render(self) -> None:
        """
        Render the engine, i.e., get all observations and send them to the interfaces
        in the case of an interface with the observer role, the observation is exactly the current state

        Warning: this method may modify the current state of the environment (the belief part).
            I.e., assert current_state_before_render ==/!== current_state_after_render.
        """
        metrics = {'episode': self.environment.current_episode,
                   'step': self.environment.current_step,
                   'agent': '',
                   'action': '',
                   'reward': ''}
        # set observations for all agents
        observation = {}
        additional_info = {}
        for ag in self.environment.agents:
            observation[ag.get_fullname()] = self.environment.get_observation_for_agent(ag)
            additional_info[ag.get_fullname()] = self.environment.get_additional_info_for_agent()
            reward = None
            if self.environment.game.is_rewarded:
                reward = self.environment.get_reward_for_agent(ag)
            ag.set_observation_reward(observation[ag.get_fullname()], reward)
            metrics['agent'] = ag.name
            metrics['action'] = ag.action.type if ag.action is not None else '-'
            metrics['reward'] = reward if reward is not None else '-'
            self.env_logger.log_metrics(metrics)

        # send observation for interface agents

        for interface in self.connected_sub_app.items():
            if (interface[1].last_info_sent['episode'] is None or
                    (interface[1].last_info_sent['episode'] < self.environment.current_episode
                     or interface[1].last_info_sent['step'] < self.environment.current_step)):
                interface[1].last_info_sent['episode'] = self.environment.current_episode
                interface[1].last_info_sent['step'] = self.environment.current_step
                if interface[1].role == ConnectedSubAppInfo.ROLE_ACTOR:
                    obs = observation[interface[1].agent_fname]
                    add_info = additional_info[interface[1].agent_fname]
                else:
                    obs = self.environment.current_state
                    add_info = self.environment.current_additional_info
                params_observation = {'observation': obs,
                                      'additional_information': add_info}
                msg = Message(Message.MESSAGE_TYPE_OBSERVATION, params_observation, self.id)
                self.send_message(msg, interface[1].id)
                self.logger.debug('Send observation : %s',observation)
                self.logger.debug('Send additional information : %s',additional_info)
            else:
                self.logger.debug('Observation already sent')
        self.old_step = self.environment.current_step

    def handle_event(self) -> None:
        """
        Handle received event. Wait for QUIT, ACTION or REGISTER
        """
        blocking = False
        current_ag_name_to_play = self.environment.game.get_system_value(self.environment.current_state,
                                                                         'AgentOrder').head
        interface_id_to_play = self.get_connected_id_from_agent_fname(current_ag_name_to_play)

        if interface_id_to_play is not None and \
                self.connected_sub_app[interface_id_to_play].role == ConnectedSubAppInfo.ROLE_ACTOR:
            blocking = True
        _ = self.wait_message([Message.MESSAGE_TYPE_QUIT_GAME,
                               Message.MESSAGE_TYPE_ACTION,
                               Message.MESSAGE_TYPE_REGISTER], blocking)
        if self.current_event is not None:
            if self.current_event.msg_type == Message.MESSAGE_TYPE_QUIT_GAME:
                # There the message is not taking into account for automated games (pymasep-examples)
                self.environment.end_episode = True
            if self.current_event.msg_type == Message.MESSAGE_TYPE_REGISTER:
                self.register(self.current_event)
                self.messages_received.task_done()

        self.environment.choose_action()
        self.logger.debug('Next Actions : %s',
                         [(a[0], a[1].type if a[1] else None) for a in self.environment.next_action.items()])

    def update(self) -> None:
        """
        Update the engine. Mainly the environment
        """

        if (self.environment.get_current_coord_method() != Game.MULTIPLAYER_COORDINATION_WAITING_ALL or
                len(self.environment.next_action) == len(self.environment.agents)):
            # next state
            self.environment.calculate_next_state()
            if self.environment.game.is_rewarded:
                self.environment.calculate_reward()
            # is this the end of the episode?
            self.environment.calculate_end_episode()
            self.logger.debug('Environment updated')
        else:
            self.logger.debug('Environment NOT updated')

    def init(self, id_episode=0) -> None:
        """
        Init an episode of the environment

        :param id_episode: ID of the episode to initialize
        """
        self.environment.current_episode = id_episode
        self.environment.current_state = self.environment.game.initialize_state(self.environment)
        self.logger.debug('State created :%s', self.environment.current_state)

    def clean(self) -> None:
        """
        Clean the engine, mainly the environment
        """
        self.environment.clear_all_state_elements()

    def run(self) -> None:
        """
        Main loop of the application.
        """
        # init the game
        self.define()

        for id_episode in range(self.environment.game.nb_episodes):
            # init game
            self.init(id_episode)

            # Send the observation to the agents' sensors
            self.render()

            # Handling game loop speed
            clock = pygame.time.Clock()

            # main loop
            while not self.environment.end_episode:
                # limiting the loop speed
                _ = clock.tick(self.eps) / 1000
                # Receive the actions from the agents
                self.handle_event()
                # update the environment
                self.update()
                # Send the observation to the agents' sensors
                self.render()

            self.clean()

        msg = Message(msg_type=Message.MESSAGE_TYPE_END_GAME, param_dict=None, src_sub_app_id=self.id)
        for interface in self.connected_sub_app.items():
            self.send_message(msg, interface[1].id)

        # close wait connection thread
        if self.remote_communication is not None:
            self.remote_communication.stop_wait_connection()
            self.remote_communication.stop_wait_announcement()

        print('Engine ended')

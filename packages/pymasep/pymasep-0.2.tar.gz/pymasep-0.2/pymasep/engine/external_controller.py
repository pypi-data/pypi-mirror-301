from xml.etree import ElementTree

from pymasep.common import State, Agent, Game, Action
from pymasep.communication import Message
from pymasep.common import Controller


class ExternalController(Controller):
    """
    External controller to receive action from an interface (local or remote)
    """

    def __init__(self, environment):
        """
        :param environment: environment for the controller
        """
        super().__init__(environment)
        self.engine = None

    def action_choice(self, observation: State, agent: Agent) -> Action:
        """
        Choose the action. Get it from the action message in the current_event of the engine.

        If the current coordination method is MULTIPLAYER_COORDINATION_TURN, Act only if it is the turn of the agent that sends the action message.
        Otherwise, the agent can act whenever he wants.

        :param observation: The observation used to choose the action.
        :param agent: The agent who chooses the action.
        :return: The action chosen for the agent.
        """
        result = None
        set_action = False
        msg_action = self.engine.current_event
        if msg_action is not None:
            if msg_action.msg_type == Message.MESSAGE_TYPE_ACTION:
                action = self.environment.create_action(xml_node=msg_action.params['action'])
                if (observation and
                        msg_action.src_sub_app_id == self.engine.get_connected_id_from_agent_fname(
                            agent.get_fullname())):
                    coord_method = self.engine.environment.get_current_coord_method(observation)
                    if coord_method == Game.MULTIPLAYER_COORDINATION_TURN:
                        next_agent = self.engine.environment.game.get_system_value(observation, 'AgentOrder').head
                        if next_agent == agent.get_fullname():
                            set_action = True
                        else:
                            set_action = False
                    else:
                        set_action = True

                if set_action:
                    self.engine.logger.info('Action received ' + str(ElementTree.tostring(msg_action.params['action'])))
                    result = action
                    self.engine.current_event = None
                else:
                    coord_method = self.environment.get_current_coord_method(observation)
                    if coord_method == Game.MULTIPLAYER_COORDINATION_TURN:
                        self.engine.logger.debug('No action selected for turn'
                                                 + self.engine.environment.game.get_system_value(observation,
                                                                                                 'AgentOrder').head
                                                 + ' '
                                                 + str(observation))
                    else:
                        self.engine.logger.info('No action received')
            else:
                self.engine.logger.info('msg received is not an action : ' + str(msg_action.msg_type))
        else:
            self.engine.logger.info('No action received')
        return result

from typing import Optional, Dict, Set, Type, cast
from xml.etree.ElementTree import Element
import uuid
from logging import WARNING

from omegaconf import DictConfig

from pymasep.common.base_object import BaseObject
from pymasep.common.agent import Agent
from pymasep.common.action import Action
from pymasep.common.state import State
from pymasep.common.controller import Controller
from pymasep.common.template import Template
from pymasep.common.game import Game
from pymasep.utils import import_from_dotted_path, setup_logger, close_logger


class Environment:
    """
    Represents the environment of the game. This object keeps all dynamic value of the game.
    """

    def __init__(self, id_env: str = None, cfg: DictConfig = None) -> None:
        """
        :param id_env: the id of the environment. If None, a new uuid will be set
        :parm cfg: the configuration of the environment
        """
        self.id: str = id_env if id_env is not None else str(uuid.uuid4())
        """ Environment id. """

        if cfg is None:
            cfg =  DictConfig({})

        self.config = cfg
        """ configuration of the environment. """

        self.end_episode: bool = False
        """ the current episode is finished """

        self.current_step: int = 0
        """ current step of the environment """

        self.current_episode: int = 0
        """ current episode of the environment """

        self.current_state: Optional[State] = None
        """ current state of the environment """

        self.current_additional_info: dict = {}
        """ current additional information of the environment, related to the current state. 
        Sort of meta information on the current state """

        self.agents: Set[Agent] = set()
        """ set of agents in the current state """

        self.controllers: Dict[str, Controller] = {}
        """ set of controllers that can be used in the environment """

        self._game: Optional[Game] = None

        self.next_action: Dict[str, Action] = {}
        """ next action to be executed in the current state """

        _level_logger = WARNING if 'logger' not in self.config else self.config.logger.level
        self.logger = setup_logger(name=self.__class__.__name__,
                                   path='logs',
                                   log_filename=self.__class__.__name__ + '-' + str(self.id) + '.log',
                                   level=_level_logger)
        """ logger for the environment tasks """

    def __del__(self):
        close_logger(self.logger)

    @property
    def game(self) -> Game:
        """
        Game of the environment.
        """
        return self._game

    @game.setter
    def game(self, g: Game) -> None:
        self._game = g

    def get_current_coord_method(self, state: Optional[State] = None) -> str:
        """
        Return the current coordination method according to the current game phase in the state

        :param state: State to check the coordination method. If None, take the current state of the environment.

        :return: The current coordinate method
        """
        if state is None:
            state = self.current_state
        game_phase = self.game.get_system_value(state, 'GamePhase')
        return self.game.coord_method[game_phase]

    def get_observation_for_agent(self, agent: Agent) -> State:
        """
        Get the current observation. Current state at the moment

        :param agent: The agent to get the observation for

        :return: The current observation
        """
        return self.game.observe_state(self.current_state, agent.get_fullname())

    def get_additional_info_for_agent(self) -> dict:
        """
        Get the current additional information. Could be filtered in the future (by agent)

        :return: The current additional information
        """
        return self.current_additional_info

    def get_reward_for_agent(self, agent: Agent) -> dict:
        """
        Get the current reward for an agent.

        :param agent: The agent to get the reward

        :return: The current reward of the agent
        """
        result = 0
        if 'reward' in self.current_additional_info:
            if agent.get_fullname() in self.current_additional_info['reward']:
                result = self.current_additional_info['reward'][agent.get_fullname()]
        return result

    def get_controller(self, agent_name: str, class_controller_: Type[Controller]) -> Controller:
        """
        Get the controller of an agent. If the controller is not created, create it.
        (Maybe I should change the name of this method...)

        :param agent_name: The agent's name
        :param class_controller_: the class of the controller to create if it is not created
        :return: the instance of the agent's controller
        """
        controller = self.controllers.get(agent_name, class_controller_(environment=self))
        self.controllers[agent_name] = controller
        return controller

    def calculate_end_episode(self) -> None:
        """
        Calculate the end of the episode. Modify self.end_episode if the conditions of the episode's end are met.
        """
        self.end_episode = self.game.is_final(self.current_state) or self.end_episode
        if self.end_episode:
            self.current_state.is_final = True

    def calculate_next_state(self) -> None:
        """
        Calculate the next state of the environment.
        Change the current state.
        Increase the step
        """

        self.current_state, self.current_additional_info = self.game.next_state(current_state=self.current_state,
                                                                                actions=self.next_action)
        if 'state_changed' in self.current_additional_info and self.current_additional_info['state_changed']:
            self.current_step += 1
            self.current_state.step = self.current_step
            self.logger.debug('Current state after next state %s', self.current_state)
        else:
            self.logger.debug('State not changed nor current_step')

    def calculate_reward(self) -> None:
        """
        Calculate the reward from the current_state and add the result to additional info with key 'reward'.
        For MDP point of view, support only (at the moment) :math:`R(s)` and neither :math:`R(s,a)` nor :math:`R(s,a,s')`
        """
        self.current_additional_info['reward'] = self.game.reward(previous_state=None,
                                                                  actions=None,
                                                                  next_state=self.current_state)

    def create_base_object(self,
                           name: Optional[str] = None,
                           template: Optional[Template] = None,
                           xml_node: Optional[Element] = None,
                           parent: Optional[BaseObject] = None):
        """
        Create a base object from a string represent the type

        :param name: The identification name of the BaseObject.
        :param template: Template of the created object. \
                If None and no XML is specified, will be the default template for this bo_type
        :param xml_node: XML node used for creating the base object
        :param parent: the parent of the current object. May be None.
        :return: The BaseObject instance
        """
        # if no module is specified, the default is pymasep.common
        if xml_node is not None:
            bo_type = xml_node.tag
        else:
            bo_type = template.created_class
        if '.' not in bo_type:
            bo_type = 'pymasep.common.' + bo_type
        class_ = import_from_dotted_path(bo_type)
        if xml_node is not None:
            result = class_(environment=self, name=name, xml_node=xml_node, parent=parent)
        else:
            result = class_(environment=self, name=name, parent=parent, template=template)
        return result

    def get_type_controller(self,
                            xml_node: Optional[Element] = None,
                            template: Optional[Template] = None,
                            control: Optional[str] = None) -> Type[Controller]:
        """
        Get the type of controller according to a template or (exclusive) an XML node.

        :param xml_node: XML node used to get the controller type. Use the attribute "controller".
        :param template: The template used to get the controller type.
        :param control: 'Interface' if the agent is controlled by interface \
                (only inside engine, and if template is used)
        :return: the class of the controller to use
        """

        if template:
            class_controller_ = import_from_dotted_path(template.controller)
        else:
            class_controller_ = import_from_dotted_path(xml_node.attrib['controller'])
        return class_controller_

    def create_object(self,
                      name: Optional[str] = None,
                      template: Optional[Template] = None,
                      xml_node: Optional[Element] = None,
                      parent: Optional[BaseObject] = None,
                      control: Optional[str] = None):
        """
        Create an object. Add it into the object dictionary (if not already exists) and agent set if the object is Agent

        :param name: The identification name of the object. Not used if xml_node is used
        :param template: the template of the class to create the object. Not used if xml_node is used
        :param xml_node: XML node describing the object to create
        :param parent: the parent of the current object. Maybe None
        :param control: 'interface' if the agent is controlled by interface (only inside engine and if template is used)
        :return: the object instance
        """
        result = self.create_base_object(name=name, template=template, xml_node=xml_node, parent=parent)
        if xml_node is not None:
            result.from_xml(self, xml_node)
        if isinstance(result, Agent):
            class_controller_ = self.get_type_controller(xml_node=xml_node,
                                                         template=template,
                                                         control=control)
            result.controller = self.get_controller(result.name, class_controller_)
            if control:
                result.control = control
            self.agents.add(result)

            # put agent into an ordered list if the state contains a system object
            parent = cast(State, parent)
            if parent is not None and 'State.system' in parent.objects:
                agent_play_order = self.game.get_system_value(parent, 'AgentOrder')
                self.game.set_system_value(parent, 'AgentOrder',
                                           self.game.order_agents(agent_play_order, result))
        return result

    def create_action(self, action_type: Optional[int] = None, xml_node: Element = None) -> Action:
        """
        Create an action

        :param action_type: The type of the action (Constants in Action class)
        :param xml_node: XML to create Action

        :return: The Action created from XML or with just a type
        """
        result = Action(environment=self, action_type=action_type, xml_node=xml_node)
        if xml_node is not None:
            result.from_xml(self, xml_node)
        return result

    def choose_action(self) -> None:
        """
        Tell all agents to choose their action
        """
        current_coord_method = self.get_current_coord_method()
        if current_coord_method != Game.MULTIPLAYER_COORDINATION_WAITING_ALL \
                or (current_coord_method == Game.MULTIPLAYER_COORDINATION_WAITING_ALL and
                    len(self.next_action) == len(self.agents)):
            self.next_action.clear()

        if current_coord_method == Game.MULTIPLAYER_COORDINATION_TURN:
            current_ag_name_to_play = self.game.get_system_value(self.current_state, 'AgentOrder').head
            current_ag_to_play = [ag for ag in self.agents if ag.get_fullname() == current_ag_name_to_play][0]

            current_ag_to_play.choose_action()
            if current_ag_to_play.action:
                self.logger.debug('choose_action() %s %s',current_ag_to_play.name, str(current_ag_to_play.action))
            else:
                self.logger.debug('choose_action() %s None', current_ag_to_play.name)
            if current_ag_to_play.action is not None:
                self.next_action[current_ag_to_play.get_fullname()] = current_ag_to_play.action
        if (current_coord_method == Game.MULTIPLAYER_COORDINATION_WAITING_ALL
                or current_coord_method == Game.MULTIPLAYER_COORDINATION_FREE_FOR_ALL):
            for ag in self.agents:
                if ag.get_fullname() not in self.next_action:
                    ag.choose_action()
                if ag.action is not None:
                    self.next_action[ag.get_fullname()] = ag.action
        self.logger.debug('%s', [(a[0], str(a[1])) for a in self.next_action.items()])

    def clear_all_state_elements(self) -> None:
        """
        Clear all in the environment
        """
        self.agents.clear()
        self.next_action.clear()
        self.current_state = None
        self.current_additional_info = dict()
        self.current_step = 0
        self.end_episode = False

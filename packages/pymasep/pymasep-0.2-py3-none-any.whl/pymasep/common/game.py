from typing import Dict, Tuple, Optional, List, final, Any
import os
import json
import xml.etree.ElementTree as Et

from omegaconf import OmegaConf, DictConfig

from pymasep.common.agent import Agent
from pymasep.common.state import State
from pymasep.common.action import Action
from pymasep.common.template import Template, SYSTEM_TEMPLATES
from pymasep.common.initializer import Initializer
from pymasep.circular_head_list import CircularHeadList


class Game:
    """
    Represents the rules of the game.
    A game contains templates and initializers.
    """

    ACTION_NO_ACTION = 0
    """ No action """

    ACTION_INIT_OBJECT = 1000
    """ Action for initializing object from interface """

    ACTION_INTENTION = 2000
    """ The agent wants to validate an intention """

    ACTION_VIDEO_ENDED = 10000
    """ The interface agent wants to stop a video. See CutSceneInterfaceState"""

    MULTIPLAYER_COORDINATION_TURN = 1
    """ Turn by turn game """

    MULTIPLAYER_COORDINATION_WAITING_ALL = 2
    """Waiting all action before next state. Not implemented for interface agents at the moment."""

    MULTIPLAYER_COORDINATION_FREE_FOR_ALL = 3
    """ Execute action when it arrives. """

    def __init__(self, cfg: DictConfig = None) -> None:
        """
        :param cfg: DictConfig containing the configuration. See :ref:`config` for more information.
        """
        if cfg is None:
            cfg = OmegaConf.create()
        if cfg.get('game') is None:
            cfg['game'] = {}

        self.config = cfg
        """ configuration of the game """

        self.initializers = dict()
        """ initializers available in the game """

        self.templates = dict()
        """ templates available in the game """

        self.default_templates = dict()
        """ default templates for nature of object. Not used at the moment."""

        self.root_path = self.config['root_path']
        """ root path of the game """

        self.data_path = self.config.get('data_path', 'data')
        """ data path of the game """

        self.is_rewarded: Optional[bool] = None
        """ is the game rewards agents ? """

        self.nb_episodes = 1
        """ number of episodes of the game. Usually one except for learning/simulation games."""

        self.max_nb_players = self.config.game.get('max_nb_players', 0)
        """ maximum number of players (human) in the game """

        self.possible_players = ['player' + str(p) for p in range(self.max_nb_players)]
        """ list of possible players names """

        self.add_templates()
        self.add_initializers()

        # agent coordination management
        self.coord_method = dict()
        """ possible coordinates methods according to the game phase (see State.system object, GamePhase) """
        self.define_coord_methods()

    def define_coord_methods(self):
        """
        Define the dictionary of coordination methods according to the game phase
        """
        self.coord_method['play'] = Game.MULTIPLAYER_COORDINATION_TURN

    def add_templates(self) -> None:
        """
        Add default templates to the game
        """

        def _load_template(tmplts) -> None:
            if 'Templates' in tmplts:
                for template_dict in tmplts['Templates']:
                    tmpl = Template(self, template_dict)
                    self.add_template(tmpl)

        # System Object template
        # Warn unable to put this template into the system_template file since the default value is an instance
        agent_order_charac = Template(self, {"name": "AgentOrder",
                                             "created_class": "Characteristic",
                                             "value_type": "CircularHeadList",
                                             "default_value": CircularHeadList()})
        self.add_template(agent_order_charac)

        _load_template(SYSTEM_TEMPLATES)

        template_filename = os.path.join(self.root_path, self.data_path, 'templates.json')
        if os.path.isfile(template_filename):
            with open(template_filename) as json_file:
                templates = json.load(json_file)
                _load_template(templates)

    def add_initializers(self):
        """
        This method adds definitions of initializers to the game.
        """
        pass

    def init_state(self, environment) -> State:
        """
        Create the initial state of the game. Can be reimplemented in subclasses.

        :param environment: The environment.
        :return: The initial state
        """
        tree = Et.parse(os.path.join(self.root_path, self.data_path, 'state.xml'))
        xml_node = tree.getroot()
        result = environment.create_object(xml_node=xml_node, parent=None)
        return result

    @final
    def initialize_state(self, environment) -> State:
        """
        Create the initial state of the game.

        :param environment: The environment.
        :return: The initial state
        """
        result = self.init_state(environment)
        return result

    @staticmethod
    def set_system_value(state: State, key: str, value: Any) -> State:
        """
        Set a value to a system characteristic. The charac is set to "State.system" object.

        :param state: The state where the characteristic have to be set. The state is modified
        :param key: the name of the characteristic
        :param value: the value of the characteristic
        :return: the state modified
        """
        state.objects['State.system'].object_state.characteristics[key].value = value
        return state

    @staticmethod
    def get_system_value(state: State, key: str) -> Any:
        """
        Get the value of a system characteristic.

        :param state: The state where to read the value.
        :param key: The name of the characteristic. The name must exist.
        :return: The value of the characteristic
        """
        return state.objects['State.system'].object_state.characteristics[key].value

    def create_external_agent(self, env, external_id: str) -> Agent:
        """
        Create an agent for an external thread. Initialized as best as can the game do without external inputs

        :param env: The environment
        :param external_id: uuid of the external thread/sub_app
        :return: the agent
        """
        existing_agents = [ag.name for ag in env.agents]
        agent_name = [x for x in self.possible_players if x not in existing_agents]
        tree = Et.parse(os.path.join(self.root_path, self.data_path, 'player_init.xml'))
        xml_node = tree.getroot()
        result = env.create_object(name=agent_name[0], xml_node=xml_node, parent=env.current_state)
        result.control = external_id
        return result

    def next_state(self, current_state: State, actions: Dict[str, Action]) -> Tuple[State, Dict]:
        """
        Calculates the new state according to the current state and the action of the agent.
        Must be reimplemented in subclasses.

        :param current_state: The current state
        :param actions: action of the agents
        :return: the new state and the additional information about the state (may be None).
        """
        raise NotImplementedError("Please Implement this method")

    def reward(self,
               previous_state: Optional[State],
               actions: Optional[Dict[str, Action]],
               next_state: State) -> Dict:
        """
        Return the reward for all agents depending on the previous_state, actions and the next state.
        This is the general form, but each game can implement it as they want.

        :param previous_state: The previous state before actions.
        :param actions: Actions of the agents
        :param next_state: next state usually calculated by next_state()
        :return: a dictionary of the reward by agent.
        """
        raise NotImplementedError("Please Implement this method")

    def is_final(self, state: State) -> bool:
        """
        Is the state final?

        :param state: The state.
        :return: True if final, False if not
        """
        return False

    @classmethod
    def observe_state(cls, state: State, agent_fname: str) -> State:
        """
        State Observation function. Calculate the al state according to d from state pS

        :param state: The state of the environment.
        :param agent_fname: The agent full name that observes the state
        :return: the observed state. The result is a state (possibly partial and noisy) and not a general observation.
        """
        # first part: copy/filter/noise the current state
        observation = state.copy_obs(params={'obs_agt_fname': agent_fname})
        # second part: update the beliefs of the agents
        cls.update_belief(agent_fname, observation, state)
        return observation

    @classmethod
    def update_belief(cls, agent_fname: str, observation: State, state: State) -> None:
        """
        The belief of the agent is updated according to the observation and the state and is updated in the state and
        the observation. Normally, the copy made a reference to the belief so the belief is shared between state and
        observation for the agent agent_fname.

        :param agent_fname: Fullname of the agent this method updates the belief for
        :param observation: the observation used to update the belief.
        :param state: The state of the environment used to update the belief.
        """
        pass

    def add_initializer(self, initializer: Initializer) -> None:
        """
        Add an initializer into the initializer dictionary of the game

        :param initializer: The test_initializer to add
        """
        self.initializers[initializer.name] = initializer

    def add_template(self, template: Template) -> None:
        """
        Add a template into the initializer dictionary of the game

        :param template: The template to add
        """
        self.templates[template.name] = template

    def add_default_template(self, object_nature: str, template_name: str) -> None:
        """
        Add a default template into the initializer dictionary of the game

        :param object_nature: The type of object to associate
        :param template_name: the template to associate (must exist in game.templates)
        """
        self.default_templates[object_nature] = self.templates[template_name]

    @staticmethod
    def order_agents(current_order: List[str], new_agent) -> List[str]:
        """
        Implement rules to determine the order of playing agent.
        Usefull only for MULTIPLAYER_COORDINATION_TURN.
        At the moment, first in, first out order is implemented

        :param current_order: The current order of agent
        :param new_agent: the new agent to add
        :return: an ordered list of agents' names that can be used by next_state() to set the next agent that can play
        """

        result = current_order
        result.append(new_agent.get_fullname())
        return result

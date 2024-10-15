from __future__ import annotations
from typing import Optional
from xml.etree.ElementTree import ElementTree, Element

from pymasep.common.object import Object
from pymasep.utils import *


class Agent(Object):
    """
    Agent that act inside the environment
    """

    def __init__(self, environment,
                 name: str = None,
                 parent=None,
                 template=None,
                 xml_node: Optional[ElementTree] = None,
                 src_copy: Optional[Agent] = None
                 ) -> None:
        """
        :param environment: an Environment instance
        :param name: name of the Agent.
        :param xml_node: XML used to create the agent.
        :param template: Template of the agent. Needed if no xml_node.
        :param parent: Parent object (see objects hierarchy)
        :param src_copy: The Agent to copy. Needed if no xml_node or template. The copy is not made into the constructor, see copy_obs()

        :raise pymasep.common.exception.CreationException: If no XML or no template is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self.action = None
        """ next action of the agent """

        self.observation = None
        """ current observation of the agent """

        self.reward = None
        """ current reward of the agent, if pertinent """

        self.controller = None
        """ controller of the agent """

        self.control = None
        """ sub app id that control the agent (an interface or the engine) """

        self.intention = None
        """ current intention of the agent """

        self.belief = self.environment.create_object(name='belief',
                                                     template=environment.game.templates['EmptyBeliefTemplate'],
                                                     parent=self)
        """ belief of the agent """

    def choose_action(self) -> None:
        """
        Choose the next action of the agent using its controller
        """
        self.action = self.controller.action_choice(observation=self.observation,
                                                    agent=self)

    def set_observation_reward(self, observation, reward: Optional[Any] = None) -> None:
        """
        Set the observation and the reward of the agent.

        :param observation: Observation of the agent (as a State)
        :param reward: reward of the agent.
        """
        self.observation = observation
        self.reward = reward
        self.controller.on_observe(observation, reward)

    def id_str(self) -> str:
        """
        Create a string unique ID of the Agent.
        Depends on the content of the base object and the id_str of all characteristics in object_state,
        and the intention of the agent

        :return: The string unique ID
        """
        id_intention = ''
        if self.intention:
            id_intention = self.intention.id_str()
        return super().id_str() + id_intention + self.belief.id_str()

    def to_xml(self) -> Element:
        """
        Transform the Agent to XML.
        See :ref:`serialization` for more information.
        :return:  XML version of the Agent
        """
        result = super().to_xml()
        result.set('controller', classname(self.controller))
        if self.control is not None:
            result.set('control', self.control)
        if self.intention is not None:
            result.append(self.intention.to_xml())
        if self.belief is not None:
            result.append(self.belief.to_xml())
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to an Agent.
        The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the Agent is created.
        :param xml_node: The XML node containing the Agent content.

        :raise  pymasep.common.exception.CreationException: SubElement must be present if initializer is not present.
                                  At creation, Initializer must be present for all characteristics
                                  if initializer is not present for ObjectState
        """
        super().from_xml(environment, xml_node)
        if 'control' in xml_node.attrib:
            self.control = xml_node.attrib['control']
        for object_state_xml in xml_node:
            # Agent handles only Intention
            if object_state_xml.tag == 'Intention':
                if not self.intention:
                    self.intention = self.environment.create_object(name='', xml_node=object_state_xml, parent=self)
            if object_state_xml.tag == 'Belief':                self.belief = self.environment.create_object(name='', xml_node=object_state_xml, parent=self)

    def copy_obs(self, params: dict):
        """
        Deep copy the agent into a new instance (with sub BaseObjects, except the Belief)

        :param params: The agent needs the full name of the agent that observes (key: obs_agt_fname)

        Note : this method copy the reference of the parent.
        The parent should do the parent copy and assignment.
        Belief is the same (same reference) in the observation (for the agent that observes) and in the state.
        """
        result = super().copy_obs(params=params)
        result.controller = self.controller
        result.control = self.control
        if self.intention:
            result.intention = self.intention.copy_obs(params=params)
        if params['obs_agt_fname'] == self.get_fullname():
            result.belief = self.belief
        else:
            result.belief = self.environment.create_object(name='belief',
                                                         template=self.environment.game.templates['EmptyBeliefTemplate'],
                                                         parent=self)
        return result
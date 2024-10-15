from __future__ import annotations
from typing import Optional, Set
from xml.etree.ElementTree import Element

from pymasep.common.base_object import BaseObject
from pymasep.common.agent import Agent


class State(BaseObject):
    """
    State or Observation of the environment
    """

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[State] = None):
        """
        :param environment: an Environment instance
        :param name: name of the Agent.
        :param xml_node: XML used to create the state.
        :param template: Template of the state. Needed if no xml_node.
        :param parent: Parent object (see objects hierarchy)
        :param src_copy: The State to copy. Needed if no xml_node or template. The copy is not made into the constructor.

        :raise  pymasep.common.exception.CreationException: If no XML or no template or src_copy is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         xml_node=xml_node, template=template, src_copy=src_copy)
        self.agents: Set[Agent] = set()
        """ set of agent in the state. Can be different from the environment if the state is a partial observation"""

        self.objects = dict()
        """ Objects in the state"""

        if template is not None:
            for sub_template in template.subclass_templates:
                obj = self.environment.create_object(name=sub_template.name_base_object,
                                                     template=sub_template,
                                                     parent=self)
                self.add_object(obj)

        self.is_final: bool = False
        """ is the state final of an episode? """

        self.step: int = 0
        """ current step of the episode. """

    @BaseObject.state.getter
    def state(self) -> str:
        """
        State of the State (hum...).
        "Init" if one of its objects is in init state.

        :return: The state of the Object
        """
        result = 'run'
        for o in self.objects.values():
            if o.state == 'init':
                result = 'init'
        return result

    def id_str(self) -> str:
        """
        Create a string unique ID of the State.
        Depends on the content of the base object and the id_str of all objects in the state

        :return: The string unique ID
        """
        ordered_objects = sorted(self.objects.keys())
        id_objects = ''
        for o in ordered_objects:
            id_objects += self.objects[o].id_str()
        return super().id_str() + id_objects

    def __eq__(self, other):
        """
        Test the equality of two states. Two states are equals if they have the same type and their id_str() are equals.
        Note : in some extreme cases, two different states can have the same id_str() but should not be equals.
        This case may occur, for example, with characteristic name `Name` and `Name0` with `Name='00'` and `Name0='0'`. But you have to
        have a twisted mind to model the state this way. Please don't :) The code will remain simpler :)
        """
        if type(other) is type(self):
            return self.id_str() == other.id_str()
        return False

    def add_object(self, obj) -> None:
        """
        Add an object into the state. The object is added in self.agents if the object is an Agent

        :param obj: Object to add into state.
        """
        obj.parent = self
        self.objects[obj.get_fullname()] = obj
        if isinstance(obj, Agent):
            self.agents.add(obj)

    def to_xml(self) -> Element:
        """
        Transform the State to XML.z See :ref:`serialization` for more information.

        :return: XML version of the State
        """
        result = super().to_xml()
        result.set('is_final', str(self.is_final))
        result.set('env_step', str(self.step))
        for obj in self.objects.values():
            obj_element = obj.to_xml()
            result.append(obj_element)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to a State. The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the State is created.
        :param xml_node: The XML node that contains the State data.

        :raise  pymasep.common.exception.CreationException: SubElement must be present if initializer is not present.
                                  At creation, Initializer must be present for all characteristics
                                  if initializer is not present for ObjectState
        """
        super().from_xml(environment=environment, xml_node=xml_node)
        if 'is_final' in xml_node.attrib:
            self.is_final = (xml_node.attrib['is_final'] == 'True')
        else:
            self.is_final = False
        if 'env_step' in xml_node.attrib:
            self.step = int(xml_node.attrib['env_step'])
        if 'template' in xml_node.attrib:
            state_tmpl = self.environment.game.templates[xml_node.attrib['template']]
            for object_tmpl in state_tmpl.subclass_templates:
                new_object = self.environment.create_object(name=object_tmpl.name_base_object,
                                                            template=object_tmpl,
                                                            parent=self)
                self.add_object(new_object)
        for object_xml in xml_node:
            obj = environment.create_object(name=None, xml_node=object_xml, parent=self)
            self.add_object(obj)

    def copy_obs(self, params: dict):
        """
        Deep copy the State to a new instance.

        :param params: Not used in this method.

        """
        result = super().copy_obs(params=params)
        result.is_final = self.is_final
        result.step = self.step
        for k_o, obj in self.objects.items():
            result.add_object(obj.copy_obs(params=params))
        return result


from __future__ import annotations
from typing import Optional

from xml.etree.ElementTree import Element

from pymasep.common.base_object import BaseObject
from pymasep.common.action import Action


class Intention(BaseObject):
    """
    An intention is a desired action. This class stores all intentions of an agent

    The intention is attached to the agent when it has been validated by the game rules.
    """

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent=None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[Intention] = None
                 ):
        """
        :param environment: the environment
        :param name: name of the BaseObject
        :param xml_node: XML used to create the object.
        :param template: Template of the base object. Needed if no xml_node.
        :param parent: Parent object (see objects hierarchy)
        :param src_copy: The Intention to copy. Needed if no xml_node or template. The copy is not made into the constructor.

        :raise  pymasep.common.exception.CreationException: If no XML or no template or src_copy is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self.name: str = 'intention'
        """ the name of the object intention """

        self.intentions = []
        """ list of intentions. The order reflects the desired order of the agent """

        self.state: str = 'run'

    def add_intention(self, intention: Action) -> None:
        """
        add an intention to the agent intentions list

        :param intention: the intention (an action) to add
        """
        self.intentions.append(intention)

    def id_str(self) -> str:
        """
        Create an str unique ID of the Intention.

        :return: the string unique ID
        """
        id_str_actions = ''
        for a in self.intentions:
            id_str_actions += a.id_str()
        return super().id_str() + id_str_actions

    def to_xml(self) -> Element:
        """
        Transform the Intention to XML. See :ref:`serialization` for more information.

        :return: XML version of the Intention
        """
        result = super().to_xml()
        for one_intention in self.intentions:
            intention_element = one_intention.to_xml()
            result.append(intention_element)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to an Intention. The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the BaseObject is created.
        :param xml_node: The XML node that contains the intention data.
        """
        super().from_xml(environment=environment, xml_node=xml_node)
        for action_xml in xml_node:
            action = self.environment.create_action(xml_node=action_xml)
            self.add_intention(action)

    def copy_obs(self, params: dict):
        """
        Deep copy the Intention to a new instance.

        :param params: Not used in this method.

        Note :  this method copy the reference of the parent. The parent should do the parent copy and assignment
        """
        result = super().copy_obs(params=params)
        for i in self.intentions:
            result.intentions.append(i.copy_obs(params=params))

        return result

from __future__ import annotations
from typing import Optional, Any
from copy import deepcopy
from xml.etree.ElementTree import Element, tostring

from pymasep.common.exception import CreationException
from pymasep.utils import native_type_to_xml, native_type_from_xml, native_xml_types, method_exists


class Action:
    """
    This class represents an action that can be done by an agent.
    """

    def __init__(self, environment, action_type: Optional[int] = None,
                 xml_node: Element = None,
                 src_copy: Optional[Action] = None) -> None:
        """
        :param environment: the environment where the action is created.
        :param action_type: Type of the action. None, if xml_node.
        :param xml_node: XML used to create the Action.
        :param src_copy: The Action will be copied. See copy_obs().

        :exception pymasep.common.exception.CreationException: Raised when xml_node, action_type and src_copy are None.
        """
        self.environment = environment

        if xml_node is None and action_type is None and src_copy is None:
            raise CreationException('Need action_type, xml_node or src_copy')

        self.type: Optional[int] = action_type
        """ type of the action. May be initialized later if the action is created from xml """

        self.params = {}
        """ parameters of the actions"""

    def add_parameter(self, name: str, value: Any) -> None:
        """
        Add a parameter to the action.

        :param name: Name of the parameter.
        :param value: Value of the parameter. Must be XML serializable.
        """
        self.params[name] = value

    def id_str(self) -> str:
        """
        Create a string unique ID of the Action.
        Depends on the content of the Action (parameters).

        :return: The string unique ID
        """
        params_str = ''
        ordered_params = sorted(self.params.keys())
        for p in ordered_params:
            if method_exists(self.params[p], 'id_str'):
                id_str_params = self.params[p].id_str()
            else:
                id_str_params = str(self.params[p]).replace(' ', '')
            params_str += p + id_str_params
        return 'action' + str(self.type) + params_str

    def to_xml(self) -> Element:
        """
        Transform the Action to XML. See :ref:`serialization` for more information.

        :return: XML version of the Action
        """
        result = Element(self.__class__.__name__)
        result.set('type', str(self.type))
        for name, param in self.params.items():
            param_xml = Element('ActionParameter')
            param_xml.set('name', name)
            if method_exists(param, 'to_xml'):
                param_xml.append(param.to_xml())
            else:
                param_xml.append(native_type_to_xml(param))
            result.append(param_xml)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to an Action. The instance must be created before.
        See :ref:`serialization` for more information.

        :param environment: The environment where the Action is created.
        :param xml_node: The XML node that contains the Action values and parameters.

        """
        self.environment = environment
        self.type = int(xml_node.attrib['type'])
        for p in xml_node:
            name = p.attrib['name']
            if p[0].tag not in native_xml_types:
                if p[0].tag == 'NoneType':
                    one_param = None
                else:
                    if p[0].tag == 'Action':
                        one_param = environment.create_action(xml_node=p[0])
                    else:
                        one_param = environment.create_object(xml_node=p[0])
            else:
                value, _ = native_type_from_xml(p[0])
                one_param = value
            self.add_parameter(name, one_param)

    def __str__(self) -> str:
        return tostring(self.to_xml()).decode()

    def copy_obs(self, params: dict):
        """
        Deep copy an action into a new instance (with its parameters).

        :param params: Not directly used in this method but passed to the action parameters copy.
        """
        result = Action(environment=self.environment, action_type=self.type, src_copy=self)
        for param_name, param in self.params.items():
            if method_exists(param, 'copy_obs'):
                new_param = param.copy_obs(params=params)
            else:
                new_param = deepcopy(param)
            result.add_parameter(param_name, new_param)
        return result

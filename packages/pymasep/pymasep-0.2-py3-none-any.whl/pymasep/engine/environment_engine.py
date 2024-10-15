from typing import Type, Optional
from xml.etree.ElementTree import Element

from pymasep.common.environment import Environment
from pymasep.common.controller import Controller
from pymasep.common.template import Template
from .external_controller import ExternalController


class EnvironmentEngine(Environment):
    """
    Represents the environment of the game (Engine part). This object keeps all dynamic values of the game.\
    This environment handles all controllers for external agents (interface) as ExternalController
    """

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
        :return: the class of the controller to use. Default is ExternalController
        """
        if (xml_node is not None and 'control' in xml_node.attrib and xml_node.attrib['control'] is not None) or \
                (template and control == 'interface'):
            class_controller_ = ExternalController
        else:
            class_controller_ = super().get_type_controller(xml_node=xml_node, template=template)

        return class_controller_

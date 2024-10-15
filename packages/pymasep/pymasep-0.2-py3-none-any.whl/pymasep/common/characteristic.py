from __future__ import annotations
from typing import Any, Optional
from copy import deepcopy

from xml.etree.ElementTree import Element

import pymasep.utils
from pymasep.common import BaseObject
from pymasep.common.initializer import Initializer
from pymasep.common.exception import CreationException


class Characteristic(BaseObject):
    """
    Object to handle characteristic of an Object
    """

    def __init__(self, environment,
                 name: str = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[Characteristic] = None):
        """
        :param environment: an Environment instance
        :param name: name of the BaseObject.
        :param xml_node: XML used to create the object.
        :param template: Template of the base object. Needed if no xml_node.\
                         If the template is present, must include a value_type (see :ref:`templates`)
        :param parent: parent object (see objects hierarchy)
        :param src_copy: Characteristic to copy.
                         See copy_obs()

        :raise pymasep.common.exception.CreationException: If no XML or no template is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self._value: Any = None

        self.value_type: type = type(None)
        """ type of the characteristic value """

        if template is not None:
            self.value_type = template.value_type
            if template.default_value is not None:
                self.value = template.default_value

    @property
    def value(self) -> Any:
        """
        Value of the characteristic. The type is defined in self.value_type

        :return: The value of the characteristic
        """
        return self._value

    @value.setter
    def value(self, v: Any) -> None:
        """
        Set the value of the Characteristic.
        Change the state of the BaseObject to 'run' if the value is not set to None.

        :param v: The value to set

        :raise TypeError: If the value is not the correct type
        """
        if isinstance(v, self.value_type):
            self._value = v
            # if self._value is not None: (utilité ???)
            self.state = 'run'
        else:
            raise TypeError('value ' + str(v) + ' is not set to the correct type ' + str(self.value_type))

    def id_str(self) -> str:
        """
        Create a string unique ID of the Characteristic.
        Depends on the content of the BaseObject and the value of the Characteristic

        :return: The string unique ID
        """
        return super().id_str() + str(self.value)

    def to_xml(self) -> Element:
        """
        Transform the Characteristic to XML.
        See :ref:`serialization` for more information.

        :return: XML version of the Characteristic
        """
        result = super().to_xml()
        if self.value is not None:
            result.append(pymasep.utils.native_type_to_xml(self.value))
        else:
            result.append(pymasep.utils.native_type_to_xml_none(self.value_type))
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to a Characteristic.
        The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the BaseObject is created.
        :param xml_node: The XML node that contains Characteristic data.

        :raise  pymasep.common.exception.CreationException: Initializer or SubElement must be present.
                                  If state is 'init', the initializer must be an Interface Initializer
                                  if state is 'init', SubElement value must be None.
                                  If state is 'run', no template or initializer is allowed.
        """
        super().from_xml(environment=environment, xml_node=xml_node)

        if self.state is None:
            if 'template' in xml_node.attrib:
                charac_tmpl = self.environment.game.templates[xml_node.attrib['template']]
                self.value_type = charac_tmpl.value_type
            if len(xml_node) != 0:
                value, value_type = pymasep.utils.native_type_from_xml(xml_node[0])
                self.value_type = value_type
                self.value = value
                self.initializer = None
            else:
                if 'initializer' in xml_node.attrib:
                    initializer = self.environment.game.initializers[xml_node.attrib['initializer']]
                    self.value_type = initializer.value_type
                    initializer.apply(self)
                    if self.value is None:
                        # initializer does nothing => interface initializer => set state to init
                        self.state = 'init'
                    if self.state == 'run':
                        self.initializer = None
                else:
                    raise CreationException("Initializer or SubElement must be present.")
        else:
            if self.state == 'init':
                if 'initializer' in xml_node.attrib:
                    initializer = self.environment.game.initializers[xml_node.attrib['initializer']]
                    if initializer.init_type != Initializer.INIT_TYPE_INTERFACE:
                        raise CreationException('The initializer must be an Interface Initializer')
                    else:
                        self.value_type = initializer.value_type
                value, value_type = pymasep.utils.native_type_from_xml(xml_node[0])
                if value is not None:
                    raise CreationException('SubElement value must be None.')
                else:
                    self.value_type = value_type
            else:
                if self.state == 'run':
                    if 'template' not in xml_node.attrib and 'initializer' not in xml_node.attrib:
                        if xml_node[0].tag not in list(pymasep.utils.from_xml_types.keys()):
                            value, value_type = pymasep.utils.native_type_from_xml(xml_node[0])
                        else:
                            value = pymasep.utils.from_xml_types[xml_node[0].tag]()
                            value.from_xml(xml_node=xml_node[0])
                            value_type = pymasep.utils.from_xml_types[xml_node[0].tag]
                        self.value_type = value_type
                        self.value = value
                        self.initializer = None
                        self.template = None
                    else:
                        raise CreationException('In run mode, no template or initializer allowed')

    def copy_obs(self, params: dict):
        """
        Deep copy the Characteristic to a new instance.

        :param params: Not used for a Characteristic

        Note :  this method copy the reference of the parent.
        The parent should do the parent copy and assignment
        """
        result = super().copy_obs(params)
        result.value_type = self.value_type
        assert not isinstance(self._value, BaseObject) # Will not work if the value is a BaseObject. See MDV-71
        result._value = deepcopy(self._value)
        return result


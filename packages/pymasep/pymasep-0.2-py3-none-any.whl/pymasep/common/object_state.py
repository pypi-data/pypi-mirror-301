from __future__ import annotations
from typing import Optional

from xml.etree.ElementTree import Element

from pymasep.common import BaseObject
from pymasep.common.exception import CreationException


class ObjectState(BaseObject):
    """
    Class to handle an ObjectState of an Object
    """

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[ObjectState] = None
                 ):
        """
        :param environment: an Environment instance
        :param name: name of the ObjectState. Not used in this case, 'state' is set for ObjectState
        :param xml_node: XML used to create the object.
        :param template: Template of the object. Needed if no xml_node.
                         If the template is present, must include a value_type (see :ref:`templates`)
        :param src_copy: The ObjectState to copy. Needed if no xml_node or template. The copy is not made into the constructor.

        :raise  pymasep.common.exception.CreationException: If no XML or no template or src_copy is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self.name = 'state'
        """ name of the object state"""

        self.characteristics = dict()
        """ Characteristics of the object state"""

        if template is not None:
            for sub_template in template.subclass_templates:
                charac = self.environment.create_object(name=sub_template.name, template=sub_template, parent=self)
                self.add_characteristic(charac)

    @BaseObject.state.getter
    def state(self) -> str:
        """
        State of the ObjectState.
        "Init" if the ObjectState or one of its characteristics is in init state.

        :return: The state of the ObjectState
        """
        result = 'init' if len(self.characteristics) == 0 else 'run'
        for c in self.characteristics.values():
            if c.state == 'init':
                result = 'init'
        return result

    def add_characteristic(self, characteristic) -> None:
        """
        Adding a characteristic object inside the ObjectState. The key id of the characteristic is its name attribute

        :param characteristic: Characteristic to add.
        """
        self.characteristics[characteristic.name] = characteristic

    def id_str(self) -> str:
        """
        Create a string unique ID of the ObjectState.
        Return a concatenation of the id_str of the base object and the id_str of all characteristics

        :return: The string unique ID
        """
        ordered_charac = sorted(self.characteristics.keys())
        id_charac = ''
        for c in ordered_charac:
            id_charac += self.characteristics[c].id_str()
        return super().id_str() + id_charac

    def to_xml(self) -> Element:
        """
        Transform the ObjectState to XML including all Characteristics. See :ref:`serialization` for more information.

        :return: XML version of the ObjectState
        """
        result = super().to_xml()
        for charac in self.characteristics.values():
            charac_element = charac.to_xml()
            result.append(charac_element)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to an ObjectState. The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the ObjectState is created.
        :param xml_node: The XML node that contains the ObjectState data.

        :raise  pymasep.common.exception.CreationException: SubElement must be present if initializer is not present.
                                  At creation, Initializer must be present for all characteristics
                                  if initializer is not present for ObjectState
        """

        def create_characs_from_template(template_name):
            object_state_tmpl = self.environment.game.templates[template_name]
            for charac_tmpl in object_state_tmpl.subclass_templates:
                new_charac = self.environment.create_object(name=charac_tmpl.name,
                                                            template=charac_tmpl,
                                                            parent=self)
                self.add_characteristic(new_charac)

        def create_characs_from_subelements(xml_node_subelement):
            for charac_xml in xml_node_subelement:
                new_charac = self.environment.create_object(name=None, xml_node=charac_xml, parent=self)
                self.add_characteristic(new_charac)

        def apply_initializer(initializer_name):
            initializer = self.environment.game.initializers[initializer_name]
            initializer.apply(self)

        super().from_xml(environment=environment, xml_node=xml_node)
        if 'state' not in xml_node.attrib:
            if len(xml_node) != 0:
                if 'template' in xml_node.attrib:
                    create_characs_from_template(xml_node.attrib['template'])
                create_characs_from_subelements(xml_node)
                if 'initializer' in xml_node.attrib:
                    apply_initializer(xml_node.attrib['initializer'])
            else:
                if 'initializer' not in xml_node.attrib:
                    raise CreationException('SubElement must be present if no initializer not present')
                else:
                    if 'template' in xml_node.attrib:
                        create_characs_from_template(xml_node.attrib['template'])
                    apply_initializer(xml_node.attrib['initializer'])
            if 'initializer' in xml_node.attrib:
                for charac in [c for c in self.characteristics.values() if c.state is None]:
                    raise CreationException('Missing initializer for ' + charac.name + ' characteristic')
        else:
            if xml_node.attrib['state'] == 'init':
                if len(xml_node) != 0:
                    create_characs_from_subelements(xml_node)
                    if 'initializer' in xml_node.attrib:
                        apply_initializer(xml_node.attrib['initializer'])
            else:
                create_characs_from_subelements(xml_node)

    def check_all_init_charac_have_initializer(self, initializer) -> None:
        """
        DEPRECATED ?
        """
        if initializer is not None:
            err_charac = []
            for charac in [c for c in self.characteristics.values() if c.state == 'init']:
                if charac.name not in initializer.subclass_initializer.keys():
                    err_charac.append(charac.name)
            if err_charac:
                str_error = ','.join(err_charac)
                raise CreationException('Missing initializer for ' + str_error + ' characteristic(s)')

    def copy_obs(self, params: dict):
        """
        Deep copy the ObjectState to a new instance.

        :param params: Not used in this method.

        Note : this method copy the reference of the parent. The parent should do the parent copy and assignment
        """
        result = super().copy_obs(params)
        for c_name, c in self.characteristics.items():
            new_charac = c.copy_obs(params)
            new_charac.parent = result
            result.add_characteristic(new_charac)
        return result

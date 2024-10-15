from __future__ import annotations
from typing import Optional

from xml.etree.ElementTree import Element

from pymasep.common.base_object import BaseObject
from pymasep.common.exception import CreationException


class Object(BaseObject):
    """
    Object inside the environment
    """

    __slots__ = ['object_state', 'containers']

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[Object] = None):
        """
        :param environment: an Environment instance
        :param name: name of the Object.
        :param xml_node: XML used to create the object.
        :param template: Template of the object. Needed if no xml_node.
        :param parent: Parent object (see objects hierarchy)
        :param src_copy: The Intention to copy. Needed if no xml_node or template. The copy is not made into the constructor.

        :raise  pymasep.common.exception.CreationException: If no XML or no template or src_copy is present
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self.object_state = None
        """ the ObjectState of the object"""

        self.containers = {}
        """ all the containers of the object. """

        if template is not None:
            for sub_template in template.subclass_templates:
                # optimize to delete the test.
                if sub_template.created_class == 'ObjectState':
                    self.object_state = self.environment.create_object(name='state',
                                                                       template=sub_template,
                                                                       parent=self)
                if sub_template.created_class == 'Container':
                    if sub_template.name_base_object != 'state':
                        self.containers[sub_template.name_base_object] = self.environment.create_object(
                            name=sub_template.name_base_object,
                            template=sub_template,
                            parent=self)
                    else:
                        raise CreationException("The container cannot be named 'state'")

    @BaseObject.state.getter
    def state(self) -> str:
        """
        State of the Object.
        "Init" if the ObjectState or one of its containers is in init state.
        "Run" if the Object is operational.

        :return: The state of the Object
        """
        result = self.object_state.state
        for container in self.containers.values():
            if container.state == 'init':
                result = 'init'
        return result

    def id_str(self) -> str:
        """
        Create a string unique ID of the Object.
        Depends on the content of the base object and the id_str of all characteristics in object_state

        :return: The string unique ID
        """
        ordered_containers = sorted(self.containers.keys())
        id_containers = ''
        for c in ordered_containers:
            id_containers += self.containers[c].id_str()
        return super().id_str() + self.object_state.id_str() + id_containers

    def to_xml(self) -> Element:
        """
        Transform the Object to XML with ObjectState content
        See :ref:`serialization` for more information.

        :return: XML version of the ObjectState
        """
        result = super().to_xml()
        obj_state = self.object_state.to_xml()
        result.append(obj_state)
        if len(self.containers):
            for contained in self.containers.values():
                result.append(contained.to_xml())
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to an Object.
        The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the Object is created.
        :param xml_node: The XML node that contains the object information.

        :raise pymasep.common.exception.CreationException: SubElement must be present if initializer is not present.
                                  At creation, Initializer must be present for all characteristics
                                  if initializer is not present for ObjectState
        """

        def create_object_state_from_template(template_name):
            object_tmpl = self.environment.game.templates[template_name]
            for object_state_tmpl in object_tmpl.subclass_templates:
                if object_state_tmpl.created_class == 'ObjectState':
                    self.object_state = self.environment.create_object(name='state',
                                                                       template=object_state_tmpl,
                                                                       parent=self)
                if object_state_tmpl.created_class == 'Container':
                    cntr = self.environment.create_object(name=object_state_tmpl.name_base_object,
                                                          template=object_state_tmpl,
                                                          parent=self)
                    self.containers[cntr.name] = cntr

        def apply_initializer(initializer_name):
            initializer = self.environment.game.initializers[initializer_name]
            initializer.apply(self)

        def create_container_from_xml_node(container_xml_node):
            cntr = self.environment.create_object(name='',
                                                  xml_node=container_xml_node,
                                                  parent=self)
            self.containers[cntr.name] = cntr

        super().from_xml(environment=environment, xml_node=xml_node)
        if 'state' not in xml_node.attrib:
            if len(xml_node) != 0:
                if 'template' in xml_node.attrib:
                    create_object_state_from_template(xml_node.attrib['template'])
                for sub_object_xml in xml_node:
                    # Object handle only ObjectState and Container
                    if sub_object_xml.tag == 'ObjectState':
                        object_state = self.environment.create_object(name='',
                                                                      xml_node=sub_object_xml,
                                                                      parent=self)
                        if not self.object_state:
                            self.object_state = object_state
                        else:
                            # merge all characteristics.
                            for c in object_state.characteristics.values():
                                self.object_state.add_characteristic(c)
                    if sub_object_xml.tag == 'Container':
                        create_container_from_xml_node(sub_object_xml)
                if 'initializer' in xml_node.attrib:
                    apply_initializer(xml_node.attrib['initializer'])
            else:
                if 'initializer' not in xml_node.attrib:
                    raise CreationException('SubElement must be present if no initializer not present')
                else:
                    if 'template' in xml_node.attrib:
                        create_object_state_from_template(xml_node.attrib['template'])
                    apply_initializer(xml_node.attrib['initializer'])
            for charac in [c for c in self.object_state.characteristics.values() if c.state is None]:
                raise CreationException('Missing initializer for ' + charac.name + ' characteristic')
        else:
            for sub_object_xml in xml_node:
                # Object handle ObjectState and Container
                if sub_object_xml.tag == 'ObjectState':
                    object_state = self.environment.create_object(name='',
                                                                  xml_node=sub_object_xml,
                                                                  parent=self)
                    self.object_state = object_state
                if sub_object_xml.tag == 'Container':
                    create_container_from_xml_node(sub_object_xml)

    def add_object_in_container(self, obj, container: str):
        """
        Add an Object to a container.
        This method is currently not used, and some works need to be done to avoid the duplication of objects in state

        :param obj: The object to be added.
        :param container: The name of the container.
        """

        self.containers[container].add(obj)

    def remove_object_from_container(self, obj):
        """
        Remove an Object from its container.
        Warning: after this method, the object is not attached to anything. Should not be used at the moment. See MDV-72
        """
        self.containers[obj.parent.name].remove(obj)

    def copy_obs(self, params: dict):
        """
        Deep copy the Object to a new instance.

        :param params: Not used in this method.

        Note : this method copy the reference of the parent. The parent should do the parent copy and assignment
        """
        result = super().copy_obs(params=params)
        result.object_state = self.object_state.copy_obs(params=params)
        result.object_state.parent = result
        for cntn_name, cntn in self.containers.items():
            result.containers[cntn_name] = cntn.copy_obs(params=params)
            result.containers[cntn_name].parent = result
        return result

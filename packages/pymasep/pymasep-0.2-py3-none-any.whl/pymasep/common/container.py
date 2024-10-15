from __future__ import annotations
from typing import Optional

from xml.etree.ElementTree import Element

from pymasep.common import BaseObject
from pymasep.common.exception import CreationException, ConstraintException


class Container(BaseObject):
    """
    Container class containing other objects. A container is not an object itself, it is more an object property.
    """
    __slots__ = ['_container']

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[Container] = None
                 ):
        """
        :param environment: an Environment instance
        :param name: name of the Container.
        :param xml_node: XML used to create the Container.
        :param template: Template of the container. Needed if no xml_node.
        :param parent: Parent object (see objects hierarchy)
        :param src_copy: Container to copy. See copy_obs()
        """
        super().__init__(environment=environment, name=name, parent=parent,
                         template=template, xml_node=xml_node, src_copy=src_copy)
        self._container = {}

    @BaseObject.state.getter
    def state(self) -> str:
        """
        state of the Container. 'init' if the object is just created or if one contained object is in 'init' state.

        :return: the state of the Container
        """
        if self._state is None:
            result = 'init'  # a container is init by default until the game (or an initializer) set it to 'run'
        else:
            result = self._state
        for c in self._container.values():
            if c.state == 'init':
                result = 'init'
        return result

    def set_run(self):
        """
        Set the state of a container to run. A container must be explicitly set to run.
        """
        self.state = 'run'  # warning (readonly) by pycharm but seems to be a bug: PY-43085

    def add(self, obj):
        """
        add an object to the container.

        :param pymasep.common.Object obj: the object to add
        """
        self._container[obj.name] = obj
        obj.parent = self

    def remove(self, obj):
        """
        remove an object from the container.

        :param pymasep.common.Object obj: the object to remove
        """
        obj.parent = None
        del self._container[obj.name]

    def __iter__(self):
        return iter(self._container.values())

    def __next__(self):
        return next(iter(self._container.items()))

    def __len__(self):
        return len(self._container)

    def __getitem__(self, item):
        return self._container[item]

    def id_str(self) -> str:
        """
        Create a string unique ID of the Container.
        Return a concatenation of the id_str of the base object and the id_str of all contained objects

        :return: The string unique ID
        """
        id_container = ''
        for o_name, o in self._container.items():
            id_container += o.id_str()
        return super().id_str() + id_container

    def to_xml(self) -> Element:
        """
        Transform the Container to XML with all objects contained in the Container.
        See :ref:`serialization` for more information.

        :return: XML version of the Container

        :raise pymasep.common.exception.ConstraintException: A container not initialized must have an initializer
               before streaming to XML
        """
        result = super().to_xml()
        if self.state == 'init' and self.initializer is None:
            raise ConstraintException('A container not initialized must have an initializer before streaming')
        for obj in self._container.values():
            obj_element = obj.to_xml()
            result.append(obj_element)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to a Container.
        The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the ObjectState is created.
        :param xml_node: The XML node that contains the container information.

        :raise  pymasep.common.exception.CreationException: A container must be empty
                or containing only an initialized object.
        """
        super().from_xml(environment=environment, xml_node=xml_node)
        if self.state == 'init' and self.initializer is None:
            raise CreationException('A container not initialized must have an initializer')
        for obj_xml in xml_node:
            obj = self.environment.create_object(name=None, xml_node=obj_xml, parent=self)
            if obj.state != 'run':
                raise CreationException('A container must be empty or containing only initialized object')
            self.add(obj)

    def copy_obs(self, params: dict):
        """
        Deep copy the Container to a new instance.

        :param params: Not used for a Container

        Note : this method copy the reference of the parent. The parent should do the parent copy and assignment
        """
        result = super().copy_obs(params=params)
        for o in self._container.values():
            new_obj = o.copy_obs(params=params)
            new_obj.parent = result
            result.add(new_obj)
        return result


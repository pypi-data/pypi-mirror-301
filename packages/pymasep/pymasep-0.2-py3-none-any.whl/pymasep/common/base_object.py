from __future__ import annotations
from typing import Optional
from xml.etree.ElementTree import Element, tostring

from pymasep.common.exception import CreationException


class BaseObject:
    """
    Base class for all functional objects for pymasep that running into an environment.
    Any BaseObject can be created from template or XML. Name can be omitted if created with XML.
    """

    __slots__ = ['environment', 'name', 'nature', 'parent', 'template', '_state', 'initializer']

    def __init__(self, environment,
                 name: Optional[str] = None,
                 parent: Optional[BaseObject] = None,
                 xml_node: Optional[Element] = None,
                 template=None,
                 src_copy: Optional[BaseObject] = None) -> None:
        """
        :param environment: an Environment instance
        :param name: name of the BaseObject.
        :param xml_node: XML used to create the object.
        :param template: Template of the base object. Needed if no xml_node or src_copy
        :param parent: parent object (see objects hierarchy)
        :param src_copy: The BaseObject to copy. Needed if no xml_node or template. The copy is not made into the constructor.

        :raise  pymasep.common.exception.CreationException: If no XML or no template or src_copy is present
        """
        self.environment = environment

        self.parent = parent
        """ parent of the base object (see objects hierarchy) """

        self.name: Optional[str] = name
        """ name of the base object """

        self._state: Optional[str] = None

        self.initializer = None
        """ initializer of the base object """

        self.template = template
        """ template of the base object """

        self.nature: Optional[str] = None
        """ nature of the base object """

        if xml_node is None and template is None and src_copy is None:
            raise CreationException('Need template, xml_node or src_copy')

        if template is not None:
            self.nature = template.nature

    @property
    def state(self) -> str:
        """
        State of the BaseObject. None if the object is just created.
        "Init" if it misses something (input from user) to finish the creation. "Run" is the BaseObject is operational.

        :return: The state of the BaseObject
        """
        return self._state

    @state.setter
    def state(self, s: str) -> None:
        """
        set the state of the BaseObject.

        :param s: the state (init, run)
        """
        self._state = s

    def id_str(self) -> str:
        """
        Create a string unique ID of the BaseObject.
        Depends on the content of the BaseObject.

        :return: The string unique ID
        """
        return self.name

    def get_fullname(self) -> str:
        """
        Return the full name of the base object including the parent name : greatparentname.parentname.name.

        :return: The full name
        """
        result = self.name
        if self.parent:
            parent_fullname = self.parent.get_fullname()
            parent_fullname = parent_fullname if parent_fullname else ''
            result = parent_fullname + '.' + self.name
        return result

    def to_xml(self) -> Element:
        """
        Transform the BaseObject to XML.
        See :ref:`serialization` for more information.

        :return: XML version of the BaseObject
        """
        result = Element(self.__class__.__name__)
        result.set('name', self.name)
        if self.nature is not None:
            result.set('nature', self.nature)

        # This is one particularity of the state property. It must stay None during the XML loading (for subelement creation)
        # but never be None when serialized to XML
        state = self.state
        if self.state is None:
            state = 'init'
        result.set('state', state)

        if self.state != 'run':
            if self.initializer is not None:
                result.set('initializer', self.initializer.name)
        return result

    def from_xml(self, environment, xml_node: Element) -> None:
        """
        Transform an XML to a BaseObject.
        The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the BaseObject is created.
        :param xml_node: The XML node containing the BaseObject data.
        """
        self.name = xml_node.attrib['name'] if 'name' in xml_node.attrib else self.name
        if 'nature' in xml_node.attrib:
            self.nature = xml_node.attrib['nature']

        if 'template' in xml_node.attrib:
            bo_tmpl = self.environment.game.templates[xml_node.attrib['template']]
            self.nature = bo_tmpl.nature
            self.template = bo_tmpl

        if 'initializer' in xml_node.attrib:
            initializer = self.environment.game.initializers[xml_node.attrib['initializer']]
            self.initializer = initializer

        if 'state' in xml_node.attrib:
            self.state = xml_node.attrib['state']

    def __str__(self) -> str:
        """
        Transform the BaseObject to a string of its XML representation.
        See: ref:`serialization` for more information.

        :return: A string containing the XML representation of the object.
        """
        return tostring(self.to_xml()).decode()

    def copy_obs(self, params: dict):
        """
        Deep copy the BaseObject to a new instance.
        Template and initializer stay as the same reference as in the original.

        :param params: Parameters for the copy of a BaseObject. See each Baseobject for more information.

        Note : this method copy the reference of the parent.
        The parent should do the parent copy and assignment.
        """
        cls = self.__class__
        result = cls(name=self.name,
                     environment=self.environment,
                     template=self.template,
                     parent=self.parent,  # parent reference !
                     src_copy=self)
        result.nature = self.nature
        result.initializer = self.initializer
        result._state = self._state
        return result

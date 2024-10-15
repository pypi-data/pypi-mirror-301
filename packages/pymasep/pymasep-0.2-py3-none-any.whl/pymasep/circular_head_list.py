from collections import UserList
from xml.etree.ElementTree import Element, SubElement
import pymasep.utils


class CircularHeadList(UserList):
    """
    Implementation of a circular list with a head pointer.
    """

    def __init__(self, initlist=None) -> None:
        """
        Initialize a circular list. The list is empty by default, and head points to nothing.

        :param initlist: Initialize the circular list. Head point to the first element if initList is passed.
        """
        if initlist is None:
            initlist = []
        super().__init__(initlist=initlist)
        self._head_idx = -1
        if self.data:
            self._head_idx = 0

    @property
    def head(self):
        """
        The pointer to the head of the circular list.

        :return: The element pointed by the head
        """
        if self._head_idx != -1:
            return self.data[self._head_idx]
        return None

    def append(self, item) -> None:
        """
        Append an element at the end of the list (not circular). Change the head only if the list was empty.

        :param item: Item to add in the list
        """
        super().append(item)
        if self._head_idx == -1:
            self._head_idx = 0

    def next(self):
        """
        Return the next element of the circular list.

        :return: Return the next element. Return None if the list is empty
        """
        if self._head_idx != -1:
            return self.data[(self._head_idx + 1) % len(self.data)]
        return None

    def move_head_next(self) -> None:
        """
        Move head to the next element. Head stay None if the list is empty.
        """
        if self._head_idx != -1:
            self._head_idx = (self._head_idx + 1) % len(self.data)

    def insert(self, i: int, item) -> None:
        """
        Insert item at position i. The head remains at the same position except if the insertion is in an empty list.

        :param i: Position
        :param item: item to insert
        """
        super().insert(i=i, item=item)
        if self._head_idx == -1:
            self._head_idx = 0
        else:
            if i <= self._head_idx:
                self._head_idx += 1

    def remove(self, item) -> None:
        """
        Remove is not permitted.

        :param item: Any ite.
        :raise AttributeError: Remove is not permitted for CircularHeadList objects
        """
        raise AttributeError('Remove is not permitted for CircularHeadList objects')

    def to_xml(self) -> Element:
        """
        Transform a circular list to an XML structure.

        Format (empty list) is ``<CircularHeadList><data><list /></data><head_idx>-1</head_idx></CircularHeadList>``

        :return: An XML Element
        """
        result = Element(self.__class__.__name__)
        sub_element_data = SubElement(result, 'data')
        if self.data is not None:
            sub_element_data.append(pymasep.utils.native_type_to_xml(self.data))
        else:
            sub_element_data.append(pymasep.utils.native_type_to_xml_none(list))

        sub_element_head = SubElement(result, 'head_idx')
        sub_element_head.text = str(self._head_idx)
        return result

    def from_xml(self, xml_node: Element) -> None:
        """
        Transform all XML elements from the xml_node to the current instance.

        :param xml_node: The XML node that contains the CircularList data.
        :return: None. The current instance is modified
        """

        for elmt_xml in xml_node:
            if elmt_xml.tag == 'data':
                self.data, _ = pymasep.utils.native_type_from_xml(elmt_xml[0])
            if elmt_xml.tag == 'head_idx':
                self._head_idx = int(elmt_xml.text)

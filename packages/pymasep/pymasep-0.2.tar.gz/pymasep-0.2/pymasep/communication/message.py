from typing import Optional
from xml.etree.ElementTree import Element, fromstring
from xml.etree import ElementTree
from pymasep.utils import native_type_to_xml, native_type_from_xml


class Message:
    """
    Object send between thread or through network.

    * DEFINE: Define the game used by the engine.

      * Param: 'game': name of the game class (doted path)

    * REGISTER: Register the interface.

      * Param: 'id': id of the interface, 'queue_id': id of the queue used by interface to receive messages,\
      'role': 'InterfaceInfo.ROLE_OBSERVER' interface is only observer, 'InterfaceInfo.ROLE_ACTOR' interface is actor

    * OBSERVATION: Observation sent by engine to interface,

      * Param: 'observation': State object,\
      'additional_information': dictionary containing additional information. Ex: 'game_log', 'reward'

    * ACTION: Action sent by interface to engine

      * Param: 'action': Action object

    * END_GAME: Game is finished (by engine)

      * Param : None

    * QUI_GAME: Game is finished (by user)

      * Param : None
    """


    MESSAGE_TYPE_DEFINE = "define"
    """ I -> E : Init the initial state """

    MESSAGE_TYPE_OBSERVATION = "observation"
    """ E -> I : Observation """

    MESSAGE_TYPE_ACTION = "action"
    """ I -> E : Action """

    MESSAGE_TYPE_QUIT_GAME = "quit"
    """ I -> E : Game is finished (by user) """

    MESSAGE_TYPE_REGISTER = "register"
    """ I -> E : Register interface to engine """

    MESSAGE_TYPE_END_GAME = "end"
    """ E -> I : Game is finished (by engine) """

    def __init__(self, msg_type:str, param_dict:Optional[dict], src_sub_app_id) -> None:
        """
        :param msg_type: type of message. See above.
        :param param_dict: Parameters of the message. May be None.
        :param src_sub_app_id: SubApplication id that send the message.
        """
        self.msg_type = msg_type
        """ type of the message. See MESSAGE_TYPE_*"""

        self.params = param_dict
        """ parameter of the message"""

        self.src_sub_app_id = src_sub_app_id
        """ id of the sub application (interface or engine) source of the message"""

    def to_xml(self) -> Element:
        """
        Transform the Message to XML.

        :return: XML version of the Message
        """
        result = Element(self.__class__.__name__)
        result.set('msg_type', self.msg_type)
        result.set('src_sub_app', self.src_sub_app_id)
        if self.params:
            param_xml = native_type_to_xml(self.params)
            result.append(param_xml)
        return result

    def from_xml(self, xml_node: Element) -> None:
        """
        Transform an XML to a Message. The instance must be created before

        :param xml_node: The XML node containing the Message
        """
        self.msg_type = xml_node.attrib['msg_type']
        self.src_sub_app_id = xml_node.attrib['src_sub_app']
        for param_xml in xml_node:
            self.params, param_type = native_type_from_xml(param_xml)
            assert param_type == dict

    def __eq__(self, other) -> bool:
        """
        Check if two messages are equals

        :return: True if two messages are equals
        """
        return self.msg_type == other.msg_type and \
            self.params == other.params and \
            self.src_sub_app_id == other.src_sub_app_id

    def __str__(self) -> str:
        """
        Transform the message to string containing the XML version of the message

        :return: A string representing the XML version of the message
        """
        return ElementTree.tostring(self.to_xml()).decode("utf-8")

    def to_bytes(self) -> bytes:
        """
        Transform the message to bytes

        :return: The message as bytes
        """
        return ElementTree.tostring(self.to_xml())

    def from_bytes(self, b: bytes) -> None:
        """
        Transform bytes to a message.

        :param b: Bytes string representing XML
        """
        self.from_xml(xml_node=fromstring(b))

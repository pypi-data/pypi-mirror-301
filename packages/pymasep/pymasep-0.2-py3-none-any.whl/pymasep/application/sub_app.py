import queue
import uuid
from typing import List, Optional
from threading import Thread
from logging import Logger, WARNING

from omegaconf import DictConfig

from pymasep.application.sub_app_state import SubAppState
from pymasep.application.connected_sub_app_info import ConnectedSubAppInfo
from pymasep.communication.message import Message
from pymasep.communication.frame import Frame
from pymasep.communication.base_threaded_communication import BaseThreadedCommunication
from pymasep.common.environment import Environment
from pymasep.utils import setup_logger, close_logger


class SubApp(Thread):
    """
    Part of the application as a Thread. Usually a sub application is the engine or the interface.
    """

    def __init__(self, app, received_q_id: int, cfg: DictConfig) -> None:
        """
        :param App app: main application
        :param received_q_id: id of the queue used by the sub app to receive messages.
        :param cfg: configuration of the sub application
        """
        Thread.__init__(self, name=self.__class__.__name__)

        self.id: str = str(uuid.uuid4())
        """ id of the sub application """

        self.config = cfg
        """ configuration of the sub application """

        self.app = app
        """ main application pointer """

        self.messages_received_q_id = received_q_id
        """ id of the queue used to receive messages """

        self.messages_received: queue.Queue = self.app.queues[received_q_id]
        """ queue used to receive messages """

        self.connected_sub_app = {}
        """ dict of sub applications information connected to this sub application """

        self.current_event: Optional[Message] = None
        """ Last message received by the sub application """

        # State management
        self.app_states = {}
        """ possible states of the sub application """

        self.current_app_states: List[SubAppState] = []
        """ Stack of the current state of the sub application """

        # Logger
        if 'logger' not in self.config:
            self.config['logger'] = {'level': WARNING}
        self.logger: Logger = setup_logger(name=self.__class__.__name__,
                                           path='logs',
                                           log_filename=self.__class__.__name__ + '-' + str(self.id) + '.log',
                                           level=self.config.logger.level)
        """ logger for the sub application """

        self.environment: Optional[Environment] = None
        """ environment used to run the sub application """

        self.remote_communication: Optional[BaseThreadedCommunication] = None
        """ the remote communication of the sub application as a BaseThreadedCommunication (Client or Server) """

    def __del__(self):
        """
        Delete the instance. Close the logger
        """
        close_logger(self.logger)

    def register_connected_sub_app(self, sub_app_id: str, role: str, sent_q: Optional[queue.Queue] = None) -> None:
        """
        Register a sub application connected to self with a rale, and optionally a queue (if it's the same process).

        :param sub_app_id: Connected sub app id
        :param role: role of the connected sub app. See ConnectedSubAppInfo.
        :param sent_q: Queue of the connected sub app used to send messages (for sub apps in the same process)
        """
        sa_info = ConnectedSubAppInfo(sub_app_id=sub_app_id, role=role, msg_queue=sent_q)
        self.connected_sub_app[sub_app_id] = sa_info

    def get_connected_id_from_agent_fname(self, agent_fname: str) -> str:
        """
        get the connected sub app that handles an agent

        :param agent_fname: the agent full name (ex. state.agent_name)
        :return: the id of the sub app associated to the agent
        """
        result = None
        list_id = [csai.id for csai in self.connected_sub_app.values() if csai.agent_fname == agent_fname]
        if list_id:
            result = list_id[0]
        return result

    def send_message(self, message: Message, subapp_id: str) -> None:
        """
        Send messages to a sub app from its id. Send by queue or by socket according to
        the connection between the tow sub app

        :param message: Message to send
        :param subapp_id: destination sub app id
        """

        if self.connected_sub_app[subapp_id].queue is not None:
            self.send_message_to_queue(message, self.connected_sub_app[subapp_id].queue)
        else:
            self.remote_communication.send_frame_to(subapp_id, Frame(message.to_bytes()))
        self.logger.debug('Sent message %s', message.to_bytes())

    @staticmethod
    def send_message_to_queue(message: Message, q: queue.Queue) -> None:
        """
        Send a message to a queue. The message is put in the queue as byte

        :param message the message to send
        :param q the queue
        """
        q.put(message.to_bytes())

    def wait_message(self, wanted_messages: List[int],
                     block: bool = True,
                     most_recent: bool = False,
                     keep_all: Optional[List[int]] = None) -> Message:
        """
        Wait for a message of certain types. The wait can be blocked or not.
        The received message is put in self.current_event

        :param wanted_messages: List of wanted messages types.
        :param block: True if the method blocks until a message arrives
        :param most_recent: True makes the function to get the most recent message in the queue and empty the queue
        :param keep_all: List of message types that will not be skipped when most_recent is True.
                         All messages after the message with type in keep_all, are kept in the queue.
        :return: The received message
        """
        try:
            msg_byte = self.messages_received.get(block=block)
            if most_recent:
                while not self.messages_received.empty():
                    msg_byte = self.messages_received.get(block=block)
                    if keep_all and len(keep_all) > 0:
                        msg = Message(0, None, self.id)
                        msg.from_bytes(msg_byte)
                        if msg.msg_type in keep_all:
                            break

            msg = Message(0, None, self.id)
            msg.from_bytes(msg_byte)
            if msg.msg_type in wanted_messages:
                self.current_event = msg
                self.logger.debug('Received message: %s',msg.msg_type)
            else:
                self.current_event = None
                self.logger.warning('Expected: %s instead have %s',wanted_messages, msg.msg_type)
        except queue.Empty:
            self.current_event = None
        return self.current_event

    # Game state management (kind of)

    def get_current_app_state(self):
        """
        Get the current sub app state

        :return: The current sub app state as SubAppState
        """
        return self.current_app_states[-1]

    def push_state(self, sbapp_state: SubAppState) -> None:
        """
        Push a new state in the head state. Pause the current state and init the new one.

        :param sbapp_state: New state to push
        """
        if self.current_app_states:
            self.current_app_states[-1].pause()
        self.current_app_states.append(sbapp_state)
        self.current_app_states[-1].init()

    def set_state(self, sbapp_state: SubAppState) -> None:
        """
        Set a new state. Remove the ald current and push the new one.

        :param sbapp_state: New state to set
        """
        self.pop_state()
        self.push_state(sbapp_state)

    def pop_state(self) -> None:
        """
        Clean and remove the current state
        """
        if self.current_app_states:
            self.current_app_states[-1].clean()
            self.current_app_states.pop()
            self.current_app_states[-1].pause()

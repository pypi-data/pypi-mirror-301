from typing import Type, Any, Union
from threading import Lock
from logging import Logger
import socket
from logging import WARNING

from pymasep.utils import setup_logger


class BaseThreadedCommunication:
    """
    Base class for threaded communication for Client and Server
    """

    def __init__(self,
                 ident: str,
                 socket_handler_class: Type[Any],
                 socket_handler_args: tuple,
                 host: str,
                 port: int,
                 log_level: Union[str, int]):
        """
        :param ident: string id of the client or server.
        :param host: Host to listen or connect.
        :param port: Port to listen or connect.
        :param socket_handler_class: Class used to handle the socket (send, receive).
        :param socket_handler_args: Arguments as tuple to instantiate the SocketHandler class.
        :param log_level: Log level messages to log as str or int. Default is logging.WARNING.
        """
        self.id = ident
        """ id of the communication thread"""

        self.host = host
        """ host to listen or connect """

        self.port = port
        """ port to listen or connect """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4/TCP
        """ socket used to listen or connect"""

        self.logger: Logger = setup_logger(name=self.__class__.__name__,
                                           path='logs',
                                           log_filename=self.__class__.__name__ + '-' + str(self.id) + '.log',
                                           level=log_level)
        """ communication logger"""

        self.socket_handler_class = socket_handler_class
        """ class to handle message from/to socket """

        self.socket_handler_args = socket_handler_args
        """ socket handler arguments"""

        # https://stackoverflow.com/questions/13610654/how-to-make-built-in-containers-sets-dicts-lists-thread-safe
        self._current_connections = dict()  # dict (id -> SocketHandler)
        """ keep trace of current connections"""

        self._current_connections_lock = Lock()
        """ lock to handle multiple connections at the same time"""

    def add_connection(self, ident: str, sh) -> None:
        """
        Add a connection to the client or server

        :param ident: ID of the opposite BaseThreadCommunication connected to self.
        :param sh: Instance of the socket handler used to handle this connection
        """
        with self._current_connections_lock:
            self._current_connections[ident] = sh

    def get_connection(self, ident):
        """
        Get the socket handler of the connection

        :param ident: ID of the connection
        :return: the socket handler
        """
        with self._current_connections_lock:
            return self._current_connections[ident]

    def is_connection_registered(self, ident):
        """
        Check if a connection is registered in this BaseThreadCommunication.

        :param ident: ID of the connection
        :return: True if a socket handler is associated to this connection id
        """
        with self._current_connections_lock:
            return ident in self._current_connections

    def send_frame_to(self, ident: str, frame):
        """
        Send a frame to a connection identified by ident

        :param ident: ID of the connection to send a frame.
        :param frame: Frame to send.
        """
        self.get_connection(ident).send_frame_async(frame)

import socket
import struct
from typing import Type, Any, Union
from threading import Thread, Event
import logging

from pymasep.communication import BaseThreadedCommunication, Frame

import traceback


class WaitConnection(Thread):
    """
    Thread used to wait connection and creating the associated socket_handler
    """

    def __init__(self,
                 server,
                 socket_handler_class: Type[Any],
                 socket_handler_args: tuple) -> None:
        """
        :param server: the server instance
        :param socket_handler_class: class used to handle the socket (send, receive)Type[ReceiveHandler]
        :param socket_handler_args: arguments as tuple to instantiate the SocketHandler class
        """
        super().__init__(name='WaitConnection')

        self.server = server
        """ server that is waiting """

        self.socket_handler_class = socket_handler_class
        """ class to handle message """

        self.socket_handler_args = socket_handler_args
        """ arguments for the message handler """

        # Thanks ! https://riptutorial.com/python/example/31665/stoppable-thread-with-a-while-loop
        self._stop_event = Event()

    def stop(self):
        """
        Stop waiting of new connections
        """
        self._stop_event.set()
        # to unblock accept() in run()
        temp_socket = socket.socket()
        temp_socket.connect(('localhost', self.server.port))
        temp_socket.close()

    def run(self):
        """
        main loop of accepting new connections
        """
        try:
            while not self._stop_event.is_set():
                conn, addr = self.server.socket.accept()
                self.server.logger.info('Server accept connection on ' + self.server.host + ':' + str(self.server.port))
                if not self._stop_event.is_set():
                    sock_handler = self.socket_handler_class(conn, addr, self.server.logger,
                                                             *self.socket_handler_args)
                    # Init Hello dialog
                    client_hello_frame = sock_handler.receive_frame()
                    sock_handler.send_frame(Frame.hello_frame(self.server.id))
                    self.server.add_connection(client_hello_frame.message.decode('utf-8'), sock_handler)
                    self.server.logger.info(
                        'Client(id:' + client_hello_frame.message.decode('utf-8') + ') from ' + str(
                            addr) + ' connected')
                    # start socket handler
                    sock_handler.start()
                else:
                    conn.close()
        except Exception as e:
            self.server.logger.error(traceback.format_exc())
            self.server.logger.error(str(e))
            raise e


class WaitAnnouncement(Thread):
    """
    Thread used to wait a client announcement and send the server ip and port
    Thanks https://pymotw.com/2/socket/multicast.html
    """

    def __init__(self, server):
        """
        :param server: the server instance
        """
        super().__init__(name='WaitAnnouncement')
        self.server = server
        """ server that announces """

        self._stop_listen_annoucement = Event()

        multicast_group = '224.3.29.71'
        server_address = ('', 10000)
        try:
            # Create the socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Bind to the server address
            self.sock.bind(server_address)
            # Tell the operating system to add the socket to the multicast group
            # on all interfaces.
            group = socket.inet_aton(multicast_group)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        except Exception as e:
            self.server.logger.error(traceback.format_exc())
            self.server.logger.error(str(e))
            raise e

    def stop(self):
        """ stopping the announcement thread """
        self._stop_listen_annoucement.set()
        # to unblock recvfrom() in run()
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.sendto(str.encode('stop'), ('localhost', 10000))
        temp_socket.close()

    def run(self):
        """ run the announcement thread """
        try:
            while not self._stop_listen_annoucement.is_set():
                self.server.logger.info('S : waiting to receive message')
                data, address = self.sock.recvfrom(1024)
                if not self._stop_listen_annoucement.is_set():
                    self.server.logger.info('S : received %s bytes from %s' % (len(data), address[0]))
                    self.server.logger.info('S : received %s' % data.decode())
                    self.server.logger.info('S : sending acknowledgement to ' + address[0])
                    response = str(address[0]) + ':' + str(self.server.port)
                    self.sock.sendto(str.encode(response), address)
                    self.server.logger.info('S: send')
        except Exception as e:
            self.server.logger.error(traceback.format_exc())
            self.server.logger.error(str(e))
            raise e
        finally:
            self.server.logger.info('S: close')
            self.sock.close()


class Server(BaseThreadedCommunication):
    """
    Base class for Server
    """

    def __init__(self,
                 ident: str,
                 max_connection: int,
                 socket_handler_class: Type[Any],
                 socket_handler_args: tuple,
                 host: str,
                 port: int,
                 wait_announcement: bool = False,
                 log_level: Union[str, int] = logging.WARNING
                 ) -> None:
        """
        :param ident: string id of the client.
        :param host: Host to connect.
        :param port: Port to connect.
        :param max_connection: Max number of connections for the server.
        :param socket_handler_class: Class used to handle the socket (send, receive). Type[ReceiveHandler]
        :param socket_handler_args: arguments to instantiate the SocketHandler class
        :param wait_announcement: True if the server is waiting for announcements through Multicast.
        :param log_level: Log level messages to log as str or int. Default is logging.WARNING.
        """
        super().__init__(ident=ident,
                         host=host,
                         port=port,
                         socket_handler_class=socket_handler_class,
                         socket_handler_args=socket_handler_args,
                         log_level=log_level)

        self.max_connection = max_connection
        """ max number of connection for the server """

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connection)
        self.wait_connection_thread = WaitConnection(server=self,
                                                     socket_handler_class=self.socket_handler_class,
                                                     socket_handler_args=self.socket_handler_args)
        """ thread for handling new connection """
        if wait_announcement:
            self.wait_announcement_thread = WaitAnnouncement(server=self)
            """ tread for address announcement """
        else:
            self.wait_announcement_thread = None

    def __del__(self):
        """
        Delete the instance. Close the socket and stop the thread that wait connection
        and the thread that wait the announcement
        """
        self.wait_connection_thread.stop()
        if self.wait_announcement_thread:
            self.wait_announcement_thread.stop()
        self.socket.close()

    def wait_connection(self):
        """
        start the wait connection thread
        """
        self.wait_connection_thread.start()

    def stop_wait_connection(self):
        """
        stop the wait connection thread
        """
        self.wait_connection_thread.stop()

    def wait_announcement(self):
        """
        start the wait announcement thread
        """
        self.wait_announcement_thread.start()

    def stop_wait_announcement(self):
        """
        stop the wait announcement thread
        """
        self.wait_announcement_thread.stop()

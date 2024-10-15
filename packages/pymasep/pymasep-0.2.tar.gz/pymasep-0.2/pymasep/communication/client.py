import logging
from typing import Type, Any, Union
from pymasep.communication import BaseThreadedCommunication, Frame
import socket
import struct

import traceback


class Client(BaseThreadedCommunication):
    """
    Base class for Client
    """

    def __init__(self,
                 ident: str,
                 socket_handler_class: Type[Any],
                 socket_handler_args: tuple,
                 host: str = None,
                 port: int = None,
                 log_level: Union[str, int] = logging.WARNING
                 ):
        """
        :param ident: string id of the client.
        :param host: Host to connect. If None, the client will search a server to connect to.
        :param port: Port to connect. If None, the client will search a server to connect to.
        :param socket_handler_class: Class used to handle the socket (send, receive).
        :param socket_handler_args: Arguments to instantiate the SocketHandler class.
        :param log_level: Log level messages to log as str or int. Default is logging.WARNING.
        """
        super().__init__(ident=ident,
                         host=host,
                         port=port,
                         socket_handler_class=socket_handler_class,
                         socket_handler_args=socket_handler_args,
                         log_level=log_level)
        self.server_id = None
        """ id of the server to connect to"""

    def __del__(self):
        """
        Delete the instance. Close the socket
        """
        self.socket.close()

    def connect(self):
        """
        Connect the client to a server. Create the handler and register the connection.
        """
        self.socket.connect((self.host, self.port))
        clt_handler = self.socket_handler_class(self.socket, 'localhost', self.logger,
                                                *self.socket_handler_args)
        # use clt_handler because the handshake is not done and I don't have the server id
        clt_handler.send_frame(Frame.hello_frame(self.id))
        server_hello_frame = clt_handler.receive_frame()
        self.server_id = server_hello_frame.message.decode('utf-8')

        self.add_connection(self.server_id, clt_handler)

        self.logger.debug('Client (%s) connected to server (%s)',
                          self.id,
                          server_hello_frame.message.decode('utf-8'))

        clt_handler.start()

    def search_server(self):
        """
        Search a server on the local net using multicast UPD
        """
        message = b'pymasep server?'
        multicast_group = ('224.3.29.71', 10000)

        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        sock.settimeout(1)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        data = 0
        try:

            # Send data to the multicast group
            self.logger.debug('C : sending %s', message.decode())
            _ = sock.sendto(message, multicast_group)

            # Look for responses from all recipients
            while True:
                self.logger.debug('C : waiting to receive')
                try:
                    data, server = sock.recvfrom(1024)
                except socket.timeout:
                    self.logger.debug('C: timed out, no more responses')
                    if self.host is None or self.port is None:
                        self.logger.debug('C: No data received')
                        raise ConnectionError('No data received')
                    break
                else:
                    self.logger.debug('C : received %s', (data.decode(), server))
                    self.host = data.decode().split(":")[0]
                    self.port = int(data.decode().split(":")[1])
        except Exception as e:
            self.logger.error('%s',traceback.format_exc())
            self.logger.error('%s', e)
        finally:
            self.logger.debug('C : closing socket')
            sock.close()

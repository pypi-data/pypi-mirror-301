from threading import Thread, Lock
import socket
import queue
import select
from logging import Logger
from pymasep.communication import Frame


class SocketHandler(Thread):
    """
    Thread used to handle received messages from conn, addr
    """

    def __init__(self,
                 conn,
                 addr,
                 logger: Logger):
        """
        :param conn: connected socket
        :param addr: remote address
        :param logger: logger used to log send and receive message
        """

        super().__init__(name='SocketHandler')
        self.lock = Lock()
        """ lock to send/receive messages one at a time """
        self.logger = logger
        """ logger of communication """
        self.socket = conn
        """ socket to communicate """
        self.addr = addr
        """ remote address """

        # https://stackoverflow.com/questions/51104534/python-socket-receive-send-multi-threading
        self.r_sock, self.s_sock = socket.socketpair()
        """ handling multithreading """
        self.send_queue = queue.Queue()
        """ message queue for handling multithreading """

    def __del__(self):
        """
        delete the instance. close all sockets
        """
        self.r_sock.shutdown(1)
        self.s_sock.shutdown(1)
        self.r_sock.close()
        self.s_sock.close()

    def send_frame(self, frame) -> None:
        """
        send frame through socket

        :param frame: frame to send
        """
        with self.lock:
            self.socket.sendall(frame.size.to_bytes(2, 'little'))
            self.socket.sendall(frame.message)
        self.logger.debug('Send : %s',frame.message)

    def receive_frame(self) -> Frame:
        """
        wait for receiving frame from socket

        :return: received frame
        """
        with self.lock:
            length_byte = self.socket.recv(2)
            length = int.from_bytes(length_byte, 'little')
            msg = self.socket.recv(length)
        result = Frame(msg)
        self.logger.debug('Received : %s',result.message)
        return result

    def send_frame_async(self, frame):
        """
        Send a from asynchronously. Use the internal queue and socket as described here:
        https://stackoverflow.com/questions/51104534/python-socket-receive-send-multi-threading

        :param frame: Frame to send
        """
        self.send_queue.put(frame)
        self.s_sock.send(b'\x00')

    def on_receive(self, frame):
        """
        Callback when a message is received (except for BYE frame).

        :param frame: Frame received
        """
        pass

    def run(self):
        """
        Main thread run that receives and send frames
        """
        end = False
        while not end:
            rlist, _, _ = select.select([self.socket, self.r_sock], [], [])
            for ready_socket in rlist:
                if ready_socket is self.socket:
                    f = self.receive_frame()
                    if f.message == Frame.bye_frame().message:
                        end = True
                        self.logger.debug('Received frame from %s %s',self.addr, f.message)
                    else:
                        self.on_receive(frame=f)
                        self.logger.debug('Received frame from %s (on_receive()) %s', self.addr, f.message)
                else:
                    self.r_sock.recv(1)
                    m = self.send_queue.get()
                    if m.message == Frame.bye_frame().message:
                        end = True
                        self.logger.debug('Received bye frame from self')
                    self.send_frame(m)

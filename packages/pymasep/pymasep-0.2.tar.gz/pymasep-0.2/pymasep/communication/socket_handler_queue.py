from logging import Logger
from pymasep.communication import SocketHandler


class SocketHandlerQueue(SocketHandler):
    """
    Thread used to handle received messages from conn, addr.
    Put a message in a queue when received
    """

    def __init__(self,
                 conn,
                 addr,
                 logger: Logger,
                 queue):
        """
        :param conn: connected socket
        :param addr: remote address
        :param logger: logger used to log send and receive message
        :param queue: queue where the received messages are put
        """
        super().__init__(conn=conn, addr=addr, logger=logger)
        self.receive_queue = queue
        """ the queue used to receive messages"""

    def on_receive(self, frame):
        """
        Callback when a message is received (except for BYE frame). Put the frame message on the queue

        :param frame: Frame received
        """
        self.receive_queue.put(frame.message)

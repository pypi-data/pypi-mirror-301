class Frame:
    """
    Frame sent at tcp level
    """

    def __init__(self, msg: bytes):
        """
        :param msg: bytes to send
        """
        self.size = len(msg)
        if type(msg) is not bytes:
            raise TypeError('Frame message type must be bytes')
        self.message = msg

    def __eq__(self, other):
        """
        Check if two messages are equals

        :param other: The other message to compare
        :return: True if messages are equals
        """
        return self.message == other.message

    @classmethod
    def hello_frame(cls, ident: str):
        """ First frame to send at connection"""
        return Frame(str.encode(ident))

    @classmethod
    def bye_frame(cls):
        """ Frame that can be used to close the ReceivedHandler thread """
        return Frame(str.encode('BYE'))

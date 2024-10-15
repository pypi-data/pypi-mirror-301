import queue


class ConnectedSubAppInfo:
    """
    Information of a sub application connected to another one.
    """

    ROLE_NONE = 'None'
    """ No role. Testing only """

    ROLE_OBSERVER = 'Observer'
    """ The connected sub app is an Interface as observer. No action cannot be send to engine."""

    ROLE_ACTOR = 'Actor'
    """ The connected sub app is an Interface as actor. Engine will take into account the action send. """

    ROLE_SERVER = 'Server'
    """ The connected sub app is the engine """

    def __init__(self, sub_app_id: str, role: str, msg_queue: queue.Queue=None, agent_fname: str=None) -> None:
        """
        :param sub_app_id: the id of the connected sub app.
        :param role: the role of the connected sub app. See ROLE_* bellow for more information.
        :param msg_queue: the queue to send messages (in the case of intra process sub app).
        :param agent_fname: the agent fullname managed by the sub app (for interface connected sup app, None otherwise).
        """

        self.id: str = sub_app_id
        """  the id of the connected sub app """

        self.role: str = role
        """ The role of the connected sub app """

        self.queue: queue.Queue = msg_queue
        """ The queue to send message (for the case of intra process sub app)"""

        self.agent_fname = agent_fname
        """ The agent fullname managed by the sub app (for interface) """

        self.last_info_sent = {'episode': None, 'step': None}
        """ data about sent information to this sub_app by the engine """

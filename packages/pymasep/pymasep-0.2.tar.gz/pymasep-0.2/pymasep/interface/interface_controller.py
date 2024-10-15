from pymasep.common import Controller


class InterfaceController(Controller):

    def select_action(self, event) -> bool:
        """
        Selection action according to the interface event

        :param event: The event (List here all events handled by)

        :return: True if the event has been processed
        """
        pass

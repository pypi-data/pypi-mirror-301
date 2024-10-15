class SubAppState:
    """
    This class implements the concept (pretty much) of Game State but in the sub app level.
    """

    def __init__(self, sub_application):
        """
        :param  pymasep.application.SubApp sub_application: the sub application where the state is defined
        """
        self.sub_application = sub_application
        """ the sub application where the state is defined """

        self.active = False
        """ if the state is active or not """

    def init(self) -> None:
        """
        Initialisation of the state
        """
        self.active = True

    def update(self) -> None:
        """
        the update phase of the state, where variables change
        """
        raise NotImplementedError("Please Implement this method")

    def render(self, time_delta: float) -> None:
        """
        the render part : how to display the state

        :param time_delta: the time delta since the last render
        """
        raise NotImplementedError("Please Implement this method")

    def pause(self) -> None:
        """
        Pause the state
        """
        self.active = not self.active

    def clean(self) -> None:
        """
        The state is destroyed. Clean all elements of the state
        """
        self.active = False

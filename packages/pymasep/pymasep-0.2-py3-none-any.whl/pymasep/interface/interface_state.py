from pygame import Rect
from pygame_gui.core import UIContainer

from pymasep.application.sub_app_state import SubAppState


class InterfaceState(SubAppState):
    """
    This class implements the concept (pretty much) of Game State for the interface
    """

    def __init__(self, sub_application, container_dim=(100, 100)):
        """
        :param sub_application: the sub application where the state is defined
        :param container_dim: pygame_ui general container dimension (in pixel)
        """
        super().__init__(sub_application)
        self.ui_container = None
        """ pygame_gui container that include all pygame_gui elements for the state"""

        self.container_dim = container_dim
        """ dimension of the pygame_gui container """

        # possibility of for pausing state. see pause()
        #self.front_image = None


    def init(self) -> None:
        """
        Initialisation of the state
        """
        super().init()
        self.ui_container = UIContainer(Rect((0, 0), self.container_dim),
                                        manager=self.sub_application.ui_manager,
                                        object_id='#state_container')

    def clean(self) -> None:
        """
        The state is destroyed. Clean all elements of the state (including ui_container)
        """
        super().clean()
        self.ui_container.clear()

    def pause(self) -> None:
        """
        Pause the state. Change the ui_container display
        """
        super().pause()
        if self.ui_container:
            if self.active:
                #self.ui_container.enable()
                self.ui_container.show()
                #self.front_image.hide()
            else:
                #self.ui_container.disable()
                # self.front_image.show()
                self.ui_container.hide()

    def handle_event(self, event) -> None:
        """
        Handle events in the state

        :param event: The event to handle
        """
        raise NotImplementedError("Please Implement this method")

    def update(self) -> None:
        """
        The update phase of the state. For interface, it corresponds to choose action, send action and receive
        observation.
        """
        self.sub_application.choose_action()
        self.sub_application.send_action()
        self.sub_application.receive_observation()

    def render(self, time_delta) -> None:
        """
        The render part : how to display the state
        """
        pass

    def on_receive_observation(self) -> None:
        """
        Callback when the interface receives an observation
        """
        pass

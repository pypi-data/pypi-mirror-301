import pygame
from pygame import Rect
from pygame_gui.core import UIContainer
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import UILabel, UIImage


class UIInput(UIContainer):
    """
    General and abstract input with label and a value to write or select
    """

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 label_text: str,
                 waited_type: type,
                 error_resource: pygame.image):
        """
        :param relative_rect: position and size of the input
        :param manager: Manager (from pygame_gui)
        :param container: Container of the UIInput (form pygame_gui)
        :param label_text: Text of the label
        :param waited_type: Expected type of the value
        :param error_resource: Image displayed when an error occurs
        """
        super().__init__(relative_rect, manager, container=container)

        font_info = self.ui_manager.get_theme().get_font_info(self.object_ids)

        self.waited_type = waited_type
        """ expected type of the input value"""

        self.validated = True
        """ is the input valid """

        self.error_pos = Rect(0, 0, 50, self.get_size()[1])
        """ position and size of the error icon"""

        self.label_pos = Rect(self.error_pos[0] + self.error_pos[2] + 10, 0,
                              self.get_size()[0] * 0.16, int(font_info['size']) * 3)
        """ position of the label """

        _ = UILabel(relative_rect=self.label_pos,
                    container=self,
                    text=label_text + ':',
                    manager=self.ui_manager)
        self.error_image = error_resource
        """ error image displayed when an error occurs"""

        self.error = UIImage(self.error_pos, self.error_image,
                             manager=self.ui_manager, container=self)
        """ ui image for error """

        self.error.hide()

    def set_text(self, text: str):
        """
        Set the text of the input. To implement on subclasses.
        :param text: Text of the input
        """
        raise NotImplementedError("Please Implement this method")

    def get_text(self) -> str:
        """
        Set the text of the input. To implement on subclasses.

        :return: Text of the input
        """
        raise NotImplementedError("Please Implement this method")

    def update(self, time_delta: float):
        """
        Update on validating value input

        :param time_delta: Time passed since the last call
        """
        super().update(time_delta)
        if not self.validated:
            self.error.show()
        else:
            self.error.hide()

    def validate(self) -> bool:
        """
        Validate if the value of the UIInput respects some constraints

        :return: True if the value is valid
        """
        self.validated = True
        if self.get_text() != '':
            try:
                _ = self.waited_type(self.get_text())
            except ValueError:
                self.validated = False
        else:
            self.validated = False
        return self.validated

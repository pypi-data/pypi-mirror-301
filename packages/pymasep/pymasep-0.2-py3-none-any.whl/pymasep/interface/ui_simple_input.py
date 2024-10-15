from pygame import Rect, image
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import UITextEntryLine
from pymasep.interface.ui_input import UIInput


class UISimpleInput(UIInput):
    """
    Simple input with label and a value to write
    """

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 label_text: str,
                 waited_type: type,
                 error_resource: image):
        """
        :param relative_rect: Position and size of the input
        :param manager: Manager (from pygame_gui)
        :param container: Container of the UIInput (form pygame_gui)
        :param label_text: Text of the label
        :param waited_type: Expected type of the value
        :param error_resource: Image displayed when an error occurs
        """
        super().__init__(relative_rect, manager, container=container, label_text=label_text, waited_type=waited_type,
                         error_resource=error_resource)

        self.text_entry_pos = Rect((self.label_pos[0] + self.label_pos[2] + 10, 0),
                                   (self.get_size()[0] * 0.4, self.get_size()[1]))
        """ position and size of the input """
        self.text_entry_line = UITextEntryLine(relative_rect=self.text_entry_pos,
                                               manager=self.ui_manager,
                                               container=self)
        """ UI element"""

    def set_text(self, text: str):
        """
        Set the value of the input as string

        :param text: Value of the input
        """
        self.text_entry_line.set_text(text)

    def get_text(self) -> str:
        """
        Get the value of the input

        :return: Value of the input as string
        """
        return self.text_entry_line.get_text()

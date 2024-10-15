from typing import List, Tuple
from pygame import Rect, image
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import UIDropDownMenu
from pymasep.interface.ui_input import UIInput


class UIChoice(UIInput):
    """
    UI Input to choose among a list of choices
    """

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 label_text: str,
                 waited_type: type,
                 error_resource: image,
                 choices: List[Tuple[str, str]]):
        """
        :param relative_rect: Position and size of the choice.
        :param manager: Manager (from pygame_gui).
        :param container: Container of the UIChoice (form pygame_gui).
        :param label_text: Text of the label.
        :param waited_type: Expected type of the value chosen.
        :param error_resource: Image displayed when an error occurs.
        :param choices: List of choice (the first element is displayed, the second is the value)
        """
        super().__init__(relative_rect, manager, container=container, label_text=label_text, waited_type=waited_type,
                         error_resource=error_resource)

        _font_info = self.ui_manager.get_theme().get_font_info(self.object_ids)
        self.text_entry_pos = Rect((self.label_pos[0] + self.label_pos[2] + 10, 0),
                                   (self.get_size()[0] * 0.5, int(_font_info['size']) * 3))
        """ position of the label """

        self.choices = choices
        """ list of choice (1st element is displayed, 2nd is the value)"""

        self.ddmenu = UIDropDownMenu(relative_rect=self.text_entry_pos,
                                     options_list=self.choices,
                                     starting_option=self.choices[0],
                                     manager=self.ui_manager,
                                     container=self)
        """ DropDown menu """

    def set_text(self, text: str):
        """
        Set the text to display.

        :param text: Parameter is not used. First choice at initialization
        """
        self.ddmenu.selected_option = self.choices[0]

    def get_text(self) -> str:
        """
        Get the value of selected element

        :return: The second element of the chosen choice (id)
        """
        return self.ddmenu.selected_option[1]

    def update_options(self, new_options: List[Tuple[str, str]]) -> bool:
        """
        Update the options of the UIChoice.
        :param new_options: New options to set.

        :return: True if a change was made, False otherwise
        """
        result = False
        old = set(self.choices)
        new = set(new_options)
        if old != new:
            self.ddmenu.kill()
            self.ddmenu = UIDropDownMenu(relative_rect=self.text_entry_pos,
                                         options_list=new_options,
                                         starting_option=new_options[0],
                                         manager=self.ui_manager,
                                         container=self)
            self.choices = new_options
            result = True
        return result

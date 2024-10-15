import pygame
from pygame import Rect, image
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import UIButton

from pymasep.interface.ui_simple_input import UISimpleInput
from pymasep.dices import roll_dices, min_max_dices


class UIDiceSelection(UISimpleInput):
    """
    UI Input that used dices results for value
    """

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 label_text: str,
                 dices: str,
                 error_resource: image):
        """
        :param relative_rect: Position and size of the choice
        :param manager: Manager (from pygame_gui)
        :param container: Container of the UIDiceSelection (form pygame_gui)
        :param label_text: Text of the label
        :param error_resource: Image displayed when an error occurs
        """
        super().__init__(relative_rect, manager, container=container, label_text=label_text, waited_type=int,
                         error_resource=error_resource)
        self.dices = dices
        """ dices to launch. See dices.py"""

        # self.dice_pos = Rect((self.text_entry_pos[0] + self.text_entry_pos[2] + 10, 0),
        #                      (self.get_size()[0] * 0.2, self.get_size()[1]))
        self.dice_pos = Rect((self.text_entry_pos[0] + self.text_entry_pos[2] + 10, 0),
                             (-1, self.get_size()[1]))
        """ position of the dice button"""

        self.dice_button = UIButton(self.dice_pos,
                                    text=self.dices,
                                    manager=self.ui_manager,
                                    container=self,
                                    object_id='#dice_button')
        """ button to launch the dices"""

    def set_text(self, text: str):
        """
        set the result of the dices as string

        :param text: result of the dice
        """
        self.text_entry_line.set_text(text)

    def get_text(self) -> str:
        """
        return the result of the dices as string

        :return: result of the dices
        """
        return self.text_entry_line.get_text()

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process event to launch dices if the user presses the button.

        :param event: Event that could be a UI_BUTTON_PRESSED
        :return: True if the event has been processed
        """
        event_processed = super().process_event(event)

        if self.is_enabled:
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.dice_button:
                    dices_res, _ = roll_dices(self.dices)
                    self.set_text(str(dices_res))
                    event_processed = True

        return event_processed

    def validate(self) -> bool:
        """
        Validate if the value of the UIInput respects some constraints. In this case, the value of the dice must be
        between min and max value of the dice expression.

        :return: True if the value is valid
        """
        self.validated = super().validate()

        if self.validated:
            min_value, max_value = min_max_dices(self.dices)
            if int(self.get_text()) > max_value or int(self.get_text()) < min_value:
                self.validated = False

        return self.validated

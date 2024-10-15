from typing import List, Tuple

import pygame
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED
from pygame_gui.elements import UIWindow, UITextBox

from pymasep.interface.user_event import TALK_EVENT


class UIDialogBox(UIWindow):
    """
    Dialogue box to choose what to say
    """
    def __init__(self, rect: pygame.Rect, ui_manager: IUIManagerInterface, choice: List[Tuple[str, str]]) -> None:
        """
        :param rect: Rect of the dialog box.
        :param ui_manager: UIManagerInterface
        :param choice: List of tuples containing the link target (id the of dialog) and the displayed text
        """
        super().__init__(rect,
                         ui_manager,
                         window_display_title='Dialog',
                         object_id='#dialog_window',
                         resizable=False)

        self.choice = choice
        """ possible choices of talk """

        self.tb_choice = []
        """ui text box elements """

        next_y_pos = 10
        for idx_c, c in enumerate(self.choice):
            tb = UITextBox(relative_rect=pygame.Rect(0, next_y_pos, self.rect[2] - 50, -1),
                           html_text='<a href="'+c[0]+'">'+c[1]+'</a>',
                           manager=self.ui_manager,
                           container=self,
                           object_id='#dialog_font',
                           wrap_to_height=True)
            self.tb_choice.append(tb)
            next_y_pos = next_y_pos + tb.rect[3] + 10

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process the event UI_TEXT_BOX_LINK_CLICKED and post an TALK_EVENT

        :param event: The event to process.
        """
        event_processed = super().process_event(event)
        if event.type == UI_TEXT_BOX_LINK_CLICKED:
            event_talk = pygame.event.Event(TALK_EVENT,
                                            dlg_id=event.link_target)
            pygame.event.post(event_talk)
            event_processed = True
        return event_processed
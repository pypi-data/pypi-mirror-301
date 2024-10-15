from typing import Optional

from pygame import Rect, Surface, SRCALPHA
from pygame.draw import polygon
from pygame_gui.elements import UIAutoResizingContainer, UIImage
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import UITextBox
from pygame_gui import TEXT_EFFECT_TYPING_APPEAR


class UITalk(UIAutoResizingContainer):
    """
    Dialog Box to display talks
    """

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 html_text: str,
                 speaker_name: Optional[str] = None):
        """
        :param relative_rect: position and dimensions of the dialog box (pixels)
        :param manager: Manager (from pygame_gui)
        :param container: Container of the board (form pygame_gui)
        :param html_text: HTML text of the dialog box.
        :param speaker_name: Name of the speaker. If None, this part of the component is not displayed.
        """
        super().__init__(relative_rect=relative_rect,
                         manager=manager,
                         container=container)
        self.bubble_width = 20
        """ size of the bubble area """

        self.speaker_label_height = 0
        """ height of the speaker label """

        self.change_layer(101)

        self.html_text = html_text
        """ text to display on the dialog box """

        self.speaker_name_label = None
        """ speaker's name '"""

        if speaker_name is not None:
            self.speaker_label_height = 40
            self.speaker_name_label = UITextBox(manager=self.ui_manager,
                                                container=self,
                                                relative_rect=Rect(self.bubble_width - 2, 0,
                                                                   relative_rect.width,
                                                                   self.speaker_label_height),
                                                html_text='<strong>'+speaker_name+'</strong>',
                                                object_id='#talk_speaker_font')
            self.speaker_name_label.change_layer(102)
        self.talk_label = UITextBox(manager=self.ui_manager,
                                    container=self,
                                    relative_rect=Rect(self.bubble_width - 2, self.speaker_label_height,
                                                       relative_rect.width, relative_rect.height),
                                    html_text=html_text,
                                    object_id='#talk_font',
                                    wrap_to_height=True
                                    )
        """ ui label for displaying the text"""

        self.talk_label.change_layer(102)

        self.talk_label.set_active_effect(TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.005})
        self.bubble_talk = UIImage(manager=self.ui_manager,
                                   container=self,
                                   relative_rect=Rect(0, 0, self.bubble_width,
                                                      self.speaker_label_height+self.talk_label.get_relative_rect().height),
                                   image_surface=Surface(
                                       (self.bubble_width,
                                        self.speaker_label_height+self.talk_label.get_relative_rect().height),
                                       SRCALPHA))
        """ image of the bubble"""
        self.bubble_talk.change_layer(102)
        _img = Surface((self.bubble_width,self.speaker_label_height+self.talk_label.get_relative_rect().height),
                      SRCALPHA)
        polygon(_img, color=self.talk_label.background_colour,
                points=[(0, self.bubble_width),
                        (self.bubble_width, self.speaker_label_height),
                        (self.bubble_width, self.talk_label.get_relative_rect().height + self.speaker_label_height),
                        (0, self.bubble_width)],
                width=0)
        self.bubble_talk.set_image(_img)




import pygame
import pygame_gui

from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UIWindow, UILabel

import pymasep.interface.user_event as user_event
from pymasep.common.initializer import InitializerCharacInterfaceShared, InitializerCharacInterface
from pymasep.interface.ui_simple_input import UISimpleInput
from pymasep.interface.ui_dice_selection import UIDiceSelection
from pymasep.interface.ui_choice import UIChoice
from pymasep.interface.ui_merchant import UIMerchant


class UIInitObjectWindow(UIWindow):
    """
    Windows used by the user to initialize one object or agent (Characteristics in state "init")
    """

    def _get_initializer_for_charac(self, charac):
        """
        Get the initializer from the charac, or from it's ObjectState or from its Object.

        :param charac: Characteristic
        :return: the initializer for the charac
        """
        initializer = charac.initializer
        if initializer is None:
            object_to_init = self._get_object_to_init()
            initializer_obj_state = object_to_init.object_state.initializer
            if initializer_obj_state is None:
                initializer_obj = object_to_init.initializer
                initializer_obj_state = initializer_obj.subclass_initializer['objectstate']
                initializer = initializer_obj_state.subclass_initializer[charac.name]
        return initializer

    def _get_object_to_init(self):
        return self.sub_application.environment.current_state.objects[self.object_to_init_name]

    def __init__(self, rect: pygame.Rect, ui_manager: pygame_gui.UIManager, sub_application, object_to_init_name) -> None:
        """
        :param rect: Position and size of the window
        :param ui_manager: Manager (from pygame_gui)
        :param sub_application: the sub application (interface) that will handle the window
        :param object_to_init_name: name of the Object or Agent to init
        """
        super().__init__(rect,
                         ui_manager,
                         window_display_title='Init',
                         object_id='#init_window',
                         resizable=False)

        self.sub_application = sub_application
        """ interface application"""

        self.object_to_init_name = object_to_init_name
        """ name of the agent to init"""

        self.entries = {}
        """ ui entries to initialize the characteristics """

        self.set_blocking(True)

        self.font_info = self.ui_manager.get_theme().get_font_info(self.object_ids)
        """ font information to calcutate sizes"""

        self.margin = int(self.font_info['size']) / 2
        """ margin of the window"""

        self.active_player_label = UILabel(pygame.Rect((self.margin, self.margin),
                                                       (200, int(self.font_info['size']) * 1.5)),
                                           text='Joueur : ' + self.object_to_init_name,
                                           manager=self.ui_manager,
                                           container=self,
                                           object_id='#playeraction')
        """ name of the player to initialize the characteristics """

        center_x = self.rect.size[0] / 2
        pos_y = self.margin + int(self.font_info['size']) * 1.5 + self.margin

        object_to_init = self._get_object_to_init()
        charac_to_init = [c for c in object_to_init.object_state.characteristics.values() if c.state == 'init']
        for charac in charac_to_init:
            initializer = self._get_initializer_for_charac(charac)

            if initializer.value_mode == InitializerCharacInterface.VALUE_MODE_VALUE:
                self.entries[charac.name] = UISimpleInput(
                    relative_rect=pygame.Rect((self.margin, pos_y),
                                              (self.rect.size[0], int(self.font_info['size']) * 3)),
                    manager=self.ui_manager,
                    container=self,
                    label_text=charac.name,
                    waited_type=charac.value_type,
                    error_resource=self.sub_application.resources['error'])
                pos_y += self.entries[charac.name].get_size()[1] + self.margin
            if initializer.value_mode == InitializerCharacInterface.VALUE_MODE_DICE:
                self.entries[charac.name] = UIDiceSelection(
                    relative_rect=pygame.Rect((self.margin, pos_y),
                                              (self.rect.size[0], int(self.font_info['size']) * 3)),
                    manager=self.ui_manager,
                    container=self,
                    label_text=charac.name,
                    dices=initializer.param,
                    error_resource=self.sub_application.resources['error'])
                pos_y += self.entries[charac.name].get_size()[1] + self.margin
            if initializer.value_mode == InitializerCharacInterface.VALUE_MODE_CHOICE:
                self.entries[charac.name] = UIChoice(
                    relative_rect=pygame.Rect((self.margin, pos_y),
                                              (self.rect.size[0], int(self.font_info['size']) * 3 * 3)),
                    manager=self.ui_manager,
                    container=self,
                    label_text=charac.name,
                    waited_type=charac.value_type,
                    choices=initializer.filter_choice(charac.name, self.sub_application.environment.current_state),
                    error_resource=self.sub_application.resources['error'])
                pos_y += self.entries[charac.name].get_size()[1] + self.margin

        containers_to_init = [c for c in object_to_init.containers.values() if c.state == 'init']
        for container in containers_to_init:
            merchant_rect = pygame.Rect((self.margin, pos_y),
                                        (self.rect.size[0], 150))
            pos_y += 150 + self.margin

            self.merchant = UIMerchant(merchant_rect,
                                       manager=self.ui_manager,
                                       container=self,
                                       item_list=[o for o in container.initializer.obj_init.keys()],
                                       sub_application=self.sub_application,
                                       object_to_init_name=self.object_to_init_name
                                       )
            """ merchant ui to initialize containers"""

        button_rect = pygame.Rect((center_x - (self.rect.size[0] * 0.1), pos_y),
                                  (self.rect.size[0] * 0.2, -1))
        self.button_validation = UIButton(relative_rect=button_rect,
                                          text="Valider",
                                          manager=self.ui_manager,
                                          container=self,
                                          object_id='#validation_button')
        """ button to validate the initialization"""

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process the events of the windows. UI_BUTTON_PRESSED is handling on this method.

        :param event: Event to process
        :return:  True if the event has been processed
        """
        event_processed = super().process_event(event)

        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.button_validation:
                form_validated = True
                for charac_name, entry in self.entries.items():
                    form_validated &= entry.validate()
                if form_validated:
                    evt_validation = pygame.event.Event(user_event.INIT_WINDOW_VALIDATION_EVENT)
                    pygame.event.post(evt_validation)
                event_processed = True

        return event_processed

    def update(self, time_delta: float):
        """
        Update the element of the window according to the value of the shared Characteristics.
        
        :param time_delta: Time passed since the last call
        """
        object_to_init = self._get_object_to_init()
        charac_shared = [c for c in object_to_init.object_state.characteristics.values()
                         if self._get_initializer_for_charac(c).__class__ == InitializerCharacInterfaceShared]
        for c in charac_shared:
            initializer = self._get_initializer_for_charac(c)
            new_choices = initializer.filter_choice(c.name, self.sub_application.environment.current_state)
            self.entries[c.name].update_options(new_choices)

        super().update(time_delta)

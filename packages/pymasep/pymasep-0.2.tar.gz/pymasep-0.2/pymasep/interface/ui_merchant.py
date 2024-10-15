from typing import List

import pygame
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.elements import (UIPanel, UISelectionList, UIButton,
                                 UILabel)
from pygame_gui import UI_BUTTON_PRESSED

from pymasep.interface.user_event import MERCHANT_ADD_OBJECT_EVENT, MERCHANT_REMOVE_OBJECT_EVENT


class UIMerchant(UIPanel):
    """
    Interface for selecting objects to buy or to take from a container
    """

    def __init__(self, relative_rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 item_list: List[str],
                 sub_application,
                 object_to_init_name):
        """
        :param relative_rect: Position and size of the window
        :param manager: Manager (from pygame_gui)
        :param container: Container of the UIMerchant (form pygame_gui)
        :param sub_application: the sub application (interface) that will handle the panel
        :param object_to_init_name: name of the Object or Agent to init
        """
        super().__init__(relative_rect, manager=manager, container=container)

        self.sub_application = sub_application
        """ interface application"""

        self.object_to_init_name = object_to_init_name
        """ name of the agent to initialize container """

        self.selected_item_to_add = []
        """ items to add to the container"""
        self.selected_item_to_remove = []
        """ items to remove from the container"""

        self.item_list = item_list
        """ list of possible items"""

        self.label_pos = pygame.Rect(0, 0, relative_rect.size[0], 30)
        """ cost label position"""
        self.costs = UILabel(relative_rect=self.label_pos,
                             container=self,
                             text='Costs :',
                             manager=manager)
        """ cost UI label"""
        self.list_objects_rect = pygame.Rect(0, 30, relative_rect.size[0] * 0.40, relative_rect.size[1] - 10)
        """ list of possible items rectangle"""
        self.list_objects = UISelectionList(relative_rect=self.list_objects_rect,
                                            item_list=self.item_list,
                                            manager=manager,
                                            container=self
                                            )
        """ UI element of possible items"""
        self.list_objects_chosen_rect = pygame.Rect(relative_rect.size[0] * 0.50, 30,
                                                    relative_rect.size[0] * 0.40, relative_rect.size[1] - 10)
        """ chosen objects rectangle"""
        self.list_objects_chosen = UISelectionList(relative_rect=self.list_objects_chosen_rect,
                                                   item_list=[],
                                                   manager=manager,
                                                   container=self
                                                   )
        """ UI element of chosen items"""
        self.add_button = UIButton(relative_rect=pygame.Rect(relative_rect.size[0] * 0.40, 30,
                                                             relative_rect.size[0] * 0.1, 50),
                                   text="->",
                                   manager=manager,
                                   container=self)
        """ UI button to add items"""
        self.del_button = UIButton(relative_rect=pygame.Rect(relative_rect.size[0] * 0.40, 81,
                                                             relative_rect.size[0] * 0.1, 50),
                                   text="<-",
                                   manager=manager,
                                   container=self)
        """ UI button to remove items"""

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        process event to launch dices if user press the button.

        :param event: event that could be a UI_BUTTON_PRESSED
        :return: True if the event has been processed
        """
        event_processed = super().process_event(event)

        if self.is_enabled:
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.add_button:
                    if self.list_objects.get_single_selection() is not None:
                        evt_add = pygame.event.Event(MERCHANT_ADD_OBJECT_EVENT,
                                                     obj=[self.list_objects.get_single_selection()])
                        pygame.event.post(evt_add)
                        event_processed = True
                if event.ui_element == self.del_button:
                    if self.list_objects_chosen.get_single_selection() is not None:
                        evt_removed = pygame.event.Event(MERCHANT_REMOVE_OBJECT_EVENT,
                                                         obj=[self.list_objects_chosen.get_single_selection()])
                        pygame.event.post(evt_removed)
                        event_processed = True

        return event_processed

    def update(self, time_delta: float) -> None:
        """
        Update the UI element

        :param time_delta: time delta since last call
        """
        current_state = self.sub_application.environment.current_state
        ag = current_state.objects[self.object_to_init_name]
        intention = ag.intention.intentions[0] if ag.intention is not None else None
        if intention is not None and 'object' in intention.params:
            if len(self.list_objects_chosen.item_list) != len(intention.params['object']):
                self.list_objects_chosen.set_item_list([])
                self.list_objects_chosen.add_items(intention.params['object'])
                self.costs.set_text('Costs :' + str(intention.params['costs']))

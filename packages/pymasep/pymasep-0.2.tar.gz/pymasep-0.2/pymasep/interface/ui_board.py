import pygame
from pygame import Rect, Surface, SRCALPHA, KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN
from pygame.event import Event
from pygame_gui.core.interfaces import IUIManagerInterface, IContainerLikeInterface
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIImage, UITextBox

import pymasep.common
from pymasep.application.connected_sub_app_info import ConnectedSubAppInfo
import pymasep.interface.user_event as user_event

class UIBoardMode:
    """
    Base class for UIBoard modes.
    """

    def __init__(self, board):
        """
        :param board: the UIBoard where this mode is defined
        """
        self.board = board
        """ the board """


class UIBoardModeRun(UIBoardMode):
    """
    UIBoard run mode. Select the agent action when a key is pressed on the board
    """

    def process_event(self, event: Event) -> bool:
        """
        process the event received by the UIBoard

        :param event: event to process
        :return: true if the event has been processed
        """
        event_processed = False
        if self.board.sub_application.interface_role == ConnectedSubAppInfo.ROLE_ACTOR:
            if event.type == KEYDOWN:
                event_processed = self.board.sub_application.environment.controlled_agent.controller.select_action(
                    event) \
                                  or event_processed
        return event_processed

    def init(self):
        """
        Init the mode
        """
        pass

    def clean(self):
        """
        Clean the mode
        """
        pass


class UIBoardModeSelectSquare(UIBoardMode):
    """
    UIBoard select square mode. Select a square with mouse.
    """

    def process_event(self, event: Event) -> bool:
        """
        process the event received by the UIBoard

        :param event: event to process
        :return: true if the event has been processed
        """
        event_processed = False
        if event.type == MOUSEMOTION:
            mouse_pos = self.board.sub_application.ui_manager.calculate_scaled_mouse_position(event.pos)

            if self.board.hovered_board_pos is not None:
                self.board.remove_spotlight_square_state(self.board.hovered_board_pos, UIBoardSquare.STATE_HOVERED)
            self.board.hovered_board_pos = self.board.surface_pos_to_map_pos(mouse_pos)
            if 0 <= self.board.hovered_board_pos[0] < len(self.board.game_data[0]) and \
                    0 <= self.board.hovered_board_pos[1] < len(self.board.game_data):
                self.board.add_spotlight_square_state(self.board.hovered_board_pos, UIBoardSquare.STATE_HOVERED)

            event_processed = True
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.board.hovered_board_pos is not None:
                    evt_square_selected = pygame.event.Event(user_event.SQUARE_SELECTED_EVENT,
                                                             square_pos=self.board.hovered_board_pos)
                    pygame.event.post(evt_square_selected)
            if event.button == 3:
                list_pos = self.board.get_spotlight_squares_from_state(UIBoardSquare.STATE_SELECTED)
                if list_pos:
                    evt_square_validation = pygame.event.Event(user_event.SQUARE_VALIDATION_EVENT, square_pos=list_pos)
                    pygame.event.post(evt_square_validation)
        return event_processed

    def init(self) -> None:
        """
        Init the mode
        """
        pass

    def clean(self) -> None:
        """
        Clean the mode. Remove already selected square
        """
        self.board.remove_spotlight_square_state(self.board.hovered_board_pos, UIBoardSquare.STATE_HOVERED)
        self.board.hovered_board_pos = None


class UIBoardModeSelectPiece(UIBoardMode):
    """
    UIBoard select a piece on the board. Select a piece with mouse.
    """

    def process_event(self, event: Event) -> bool:
        """
        process the event received by the UIBoard

        :param event: event to process
        :return: true if the event has been processed
        """
        event_processed = False
        if event.type == MOUSEMOTION:
            if self.board.agents_tokens[self.board.player_name].hovered:
                self.board.agents_tokens[self.board.player_name].set_dimensions(
                    (self.board.square_size + 20, self.board.square_size + 20))
            else:
                self.board.agents_tokens[self.board.player_name].set_dimensions(
                    self.board.sub_application.resources[self.board.player_name].get_size())
            event_processed = True
        return event_processed

    def init(self) -> None:
        """
        Init the mode
        """
        pass

    def clean(self) -> None:
        """
        Clean the mode. Remove an already selected piece
        """
        self.board.agents_tokens[self.board.player_name].set_dimensions(
            self.board.sub_application.resources[self.board.player_name].get_size())


class UIBoardElement(UIImage):
    """
    Element that can be put on the board
    """


    STATE_HOVERED = 0
    """ The element is hovered by mouse"""

    STATE_SELECTED = 1
    """ The element is selected"""

    STATE_ERROR = 2
    """ The element is displayed as an error"""

    NB_STATES = 3
    """ max number of possible states"""

    def __init__(self, manager, board, board_pos: tuple, square_size: int, image_surface=None):
        """
        :param manager: Manager (from pygame_gui)
        :param board: Board where this element is put
        :param board_pos: Position where this element put (board coordinates)
        :param square_size: square size (in pixel)
        :param image_surface: image surface of the element to be displayed
        """
        super().__init__(relative_rect=Rect(board.map_pos_to_surface_pos(board_pos),
                                            (square_size, square_size)),
                         manager=manager,
                         container=board,
                         image_surface=image_surface)
        self.state = None
        """ state of the board element """

        self.previous_state = None
        """ previous state of the board element """

        self.square_size = square_size
        """ square size of the element """

        self.base_alpha = 150
        """ base alpha color to display over the element"""

        self.alpha = self.base_alpha
        """ current alpha color of the display over the element"""

        self.board = board
        """ board where this element is put"""

        self.base_image = pygame.surface.Surface((self.square_size, self.square_size), SRCALPHA, 32)
        """ base image surface of the element """
        pygame.transform.smoothscale(image_surface, (self.square_size, self.square_size), self.base_image)

        self._board_pos = None

        self.board_pos = board_pos
        """ position of the element """

        self.hovered_for_action = False
        """ is the element hovered in order to make an action on it"""

        self.was_hovered = False
        """ was the element hovered """


    @property
    def board_pos(self) -> tuple:
        """
        return the board position.

        :return: the board position
        """
        return self._board_pos

    @board_pos.setter
    def board_pos(self, b:tuple):
        """
        set the board position of the element

        :param b: the position (as the board coordinate system)
        """
        self._board_pos = b
        self.set_relative_position(self.board.map_pos_to_surface_pos(self.board_pos))

    def update(self, time_delta: float) -> None:
        """
        update the element.

        :param time_delta: time passed since the last call
        """
        super().update(time_delta)
        fill_color = [0, 0, 0, 0]
        if self.state is None:
            self.alpha = self.base_alpha
        if self.state == UIBoardElement.STATE_SELECTED:
            fill_color = [0, 255, 0, self.alpha]
        if self.state == UIBoardElement.STATE_ERROR:
            fill_color = [255, 0, 0, self.alpha]
            self.alpha -= self.base_alpha * time_delta
            self.alpha = max(self.alpha, 0)
        if self.was_hovered and self.hovered_for_action != self.was_hovered:
            self.set_image(self.base_image)
        if self.state is not None or self.hovered_for_action:
            self.set_image(self.base_image)
            state_surface = Surface((self.square_size, self.square_size), SRCALPHA, 32)
            state_surface.fill(fill_color)
            if self.hovered_for_action:
                hovered_surface = Surface((self.square_size, self.square_size), SRCALPHA, 32)
                h_fill_color = [255, 255, 255, self.alpha]
                hovered_surface.fill(h_fill_color)
                state_surface.blit(hovered_surface, (0, 0))
            self.image.blit(state_surface, (0, 0))
            self.image = self.image.premul_alpha()
            self.was_hovered = self.hovered_for_action


class UIBoardToken(UIBoardElement):
    """
    Token that can be put on the board. At the moment, a Token is not different from an Element
    """

    def __init__(self, manager, board, position, square_size, image_surface):
        """

        :param manager: Manager (from pygame_gui)
        :param board: Board where this element is put
        :param position: Position where this element put (board coordinates)
        :param square_size: square size (in pixel)
        :param image_surface: image surface of the element to be displayed
        """
        super().__init__(board_pos=position,
                         square_size=square_size,
                         manager=manager,
                         board=board,
                         image_surface=image_surface)


class UIBoardSquare(UIBoardElement):
    """
    Square of the board
    """

    def __init__(self, manager, board, square_size, board_pos):
        """
        :param manager: Manager (from pygame_gui)
        :param board: Board where this element is put
        :param board_pos: Position where this element put (board coordinates)
        :param square_size: square size (in pixel)
        """
        surface = Surface((square_size, square_size), SRCALPHA, 32)
        super().__init__(manager=manager,
                         board=board,
                         board_pos=board_pos,
                         square_size=square_size,
                         image_surface=surface)


class UIBoard(UIContainer):
    """
    Board with square where token can be put.

    For information, layer of elements:
      background : 90
      agents tokens: 100
      selected square: 150
    """


    RUN_MODE = 'Run'
    """ Mode of the board : Rune"""

    SELECT_SQUARE_MODE = 'SelectSquare'
    """ Mode of the board : Select a square"""

    SELECT_PIECE_MODE = 'SelectPiece'
    """ Mode of the board : Select a piece on the board"""

    def __init__(self, relative_rect: Rect,
                 manager: IUIManagerInterface,
                 container: IContainerLikeInterface,
                 sub_application,
                 image_surface: pygame.Surface,
                 game_data,
                 game_class_,
                 origin_coord_map: tuple,
                 square_size: int,
                 player_name: str
                 ):
        """
        :param relative_rect: position and dimensions of the board (pixels)
        :param manager: Manager (from pygame_gui)
        :param container: Container of the board (form pygame_gui)
        :param sub_application: sub application instance (the interface)
        :param image_surface: the image surface to display the board
        :param game_data: the data map (see @GridTools)
        :param game_class_: the class of the game
        :param origin_coord_map: pixel coordinate of the origin of the (0, 0) map position
        :param square_size: size of a square of the boad
        :param player_name: name of the player handle by the board
        """

        super().__init__(relative_rect, manager, container=container)

        self.background_image = UIImage(image_surface.get_rect(),
                                        image_surface=image_surface,
                                        manager=manager,
                                        container=self)
        """ bacground image of the board"""
        self.background_image.change_layer(90)
        self.add_element(self.background_image)

        self.game_data = game_data
        """ data of the board"""

        self.game_class_ = game_class_

        self.sub_application = sub_application
        """ interface pointer """

        self.origin_coord_map = origin_coord_map
        """ pixel origin of the (0, 0) map position """
        self.square_size = square_size
        """ square size of the element in pixel """

        self.player_name = player_name
        """ name of the player handle by the board"""

        self.agents_tokens = {}
        """ agent UITokens """
        self.objects_tokens = {}
        """ object UITokens"""

        self.spotlight_squares = {}
        """ squares that are spotlight"""

        self.hovered_board_pos = None
        """ position of the board that is hovered """

        self.modes = dict()
        """ possible mode of the board"""
        self.modes[UIBoard.RUN_MODE] = UIBoardModeRun(self)
        self.modes[UIBoard.SELECT_SQUARE_MODE] = UIBoardModeSelectSquare(self)
        self.modes[UIBoard.SELECT_PIECE_MODE] = UIBoardModeSelectPiece(self)

        self.current_mode = None
        """ current mode of the board"""

        self.board_debug_info_idx = self.sub_application.add_debug_label()
        """ idx of the board debug info """

        self.last_step_updated = None
        """ the last step when the board has been updated """

    def add_spotlight_square_state(self, board_pos, state) -> None:
        """
        Set a spotlight square at a desired state

        :param board_pos: Position on the board
        :param state: state to set see @UIBoardElement
        """
        if board_pos not in self.spotlight_squares.keys():
            # board pos not spotlighted
            self.spotlight_squares[board_pos] = {}
            spotlight_square = UIBoardSquare(self.ui_manager, self, self.square_size, board_pos)
            self.spotlight_squares[board_pos][state] = spotlight_square
            spotlight_square.show()
        else:
            # board pos spotlighted
            if state not in self.spotlight_squares[board_pos]:
                # ...but not in the desired state
                spotlight_square = UIBoardSquare(self.ui_manager, self, self.square_size, board_pos)
                spotlight_square.change_layer(150)
                self.spotlight_squares[board_pos][state] = spotlight_square
                spotlight_square.show()
            else:
                # ...in the desired state
                spotlight_square = self.spotlight_squares[board_pos][state]
        # set the new state anyway
        spotlight_square.state = state
        if state == UIBoardSquare.STATE_HOVERED:
            spotlight_square.hovered_for_action = True

    def remove_spotlight_square_state(self, board_pos, state) -> None:
        """
        Remove a spotlighted square which is at a desired state

        :param board_pos: Position on the board
        :param state: state which will be removed
        """
        if board_pos in self.spotlight_squares.keys():
            if state in self.spotlight_squares[board_pos]:
                self.spotlight_squares[board_pos][state].kill()
                del self.spotlight_squares[board_pos][state]

    def map_pos_to_surface_pos(self, map_pos) -> tuple:
        """
        Convert a map position to the surface position (pixel)

        :param map_pos: Position on the map (tuple)
        :return: surface position (tuple of pixel)
        """
        return (int(self.origin_coord_map[0] + (map_pos[0] * self.square_size)),
                self.origin_coord_map[1] + (map_pos[1] * self.square_size))

    def surface_pos_to_map_pos(self, surface_pos) -> tuple:
        """
        convert the surface position to a map position

        :param surface_pos: the surface position (pixel)
        :return: the map position (tuple)
        """
        return (int((surface_pos[0] - self.origin_coord_map[0]) / self.square_size),
                int((surface_pos[1] - self.origin_coord_map[1]) / self.square_size))

    def get_spotlight_squares_from_state(self, state):
        """
        get all the squares on the baard that are on a certain state

        :param state: state to find
        :return: List of squares
        """
        return [s for s in self.spotlight_squares.keys() if state in self.spotlight_squares[s].keys()]

    def update_with_observation(self, time_delta: float):
        """
        Part of the update directly depending on the observation and that must be called only once per observation

        :param time_delta: Time passed since the last call
        """
        state = self.sub_application.environment.current_state

        # handling object/agents
        for obj in state.objects.values():
            characs = obj.object_state.characteristics
            if 'Pos' in characs:
                object_pos = characs['Pos'].value
                if obj.name not in self.objects_tokens.keys():
                    token_name = obj.name
                    if 'Token' in obj.object_state.characteristics:
                        token_name = obj.object_state.characteristics['Token'].value
                    if token_name:
                        surface = self.sub_application.resources[token_name]
                        self.objects_tokens[obj.name] = UIBoardToken(manager=self.ui_manager,
                                                                     board=self,
                                                                     position=(0, 0),
                                                                     square_size=self.square_size,
                                                                     image_surface=surface)
                        self.objects_tokens[obj.name].change_layer(100)

                if obj.name in self.objects_tokens.keys():
                    self.objects_tokens[obj.name].board_pos = object_pos
                    if type(obj) == pymasep.common.Agent:
                        self.agents_tokens[obj.name] = self.objects_tokens[obj.name]

        # Remove non existing tokens
        # for ag_name in self.agents_tokens.keys():
        #     if ag_name not in state.objects.keys():
        #         self.agents_tokens[ag_name].kill()

    def update(self, time_delta: float):
        """
        Update the element of the board according to the observation

        :param time_delta: Time passed since the last call
        """

        state = self.sub_application.environment.current_state
        if self.last_step_updated is None or self.last_step_updated < state.step:
            self.update_with_observation(time_delta)

        super().update(time_delta)

        for p in self.spotlight_squares.keys():
            for s in range(UIBoardSquare.NB_STATES):
                if s in self.spotlight_squares[p]:
                    self.spotlight_squares[p][s].update(time_delta)
                    # remove non visible spotlight squares
                    if self.spotlight_squares[p][s].alpha == 0:
                        self.remove_spotlight_square_state(p, s)

        self.sub_application.debug_info_labels[self.board_debug_info_idx].set_text(
            f'Mouse board pos: {self.surface_pos_to_map_pos(self.ui_manager.get_mouse_position())}')

        state = self.sub_application.environment.current_state
        self.last_step_updated = state.step

    def process_event(self, event: Event) -> bool:
        """
        Process an event on the board.

        :param event: The event to process
        :return: True the event has been processed
        """
        event_processed = super().process_event(event)

        if self.is_enabled:
            event_processed = event_processed or self.modes[self.current_mode].process_event(event)

        return event_processed

    def set_mode(self, mode) -> None:
        """
        Set the mode of the board.
        :param mode: Mode of the board.
        """
        if self.current_mode is not None:
            self.modes[self.current_mode].clean()
        self.current_mode = mode
        self.modes[self.current_mode].init()

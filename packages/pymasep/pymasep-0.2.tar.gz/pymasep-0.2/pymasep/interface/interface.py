from typing import Optional
from xml.etree import ElementTree

from omegaconf import DictConfig, OmegaConf

import pygame
from pygame.locals import *
from pygame_gui import UIManager
from pygame_gui.windows import UIConsoleWindow
from pygame_gui.elements import UILabel

import pymasep as pm
from pymasep.communication import Message, Client, SocketHandlerQueue, Frame
from pymasep.application.sub_app import SubApp
from pymasep.application.connected_sub_app_info import ConnectedSubAppInfo
from pymasep.common.exception import CreationException
from pymasep.utils import LazyXMLString


class Interface(SubApp):
    """
    Sub application that displays an environment and interact with user
    """

    def __init__(self, app, received_q_id,
                 cfg: DictConfig,
                 game_class_=None,  # None for subclass, mandatory in the base class
                 interface_role=None,  # None for subclass, mandatory in the base class
                 remote_engine_host: Optional[str] = None,
                 remote_engine_port: Optional[int] = None,
                 search_remote: bool = False):
        """
        :param app: main application
        :param received_q_id: id of the queue used by the sub app to receive messages.
        :param cfg: Configuration of the interface.
        :param game_class_: Class of the game.
        :param interface_role: Role of the interface. See @ConnectedSubAppInfo.
        :param remote_engine_host: Host of the remote engine. May be None if interface is in the same process of engine.
        :param remote_engine_port: Port of the remote engine. May be None if interface is in the same process of engine.
        :param search_remote: True if the interface has to search the server on LAN. Default False

        :raise ConnectionError: If the interface does not find a server on the LAN.
        """
        super().__init__(app=app, received_q_id=received_q_id, cfg=cfg)
        # display related information
        self.screen = None
        """ screen to display on"""

        self.virtual_screen = None
        """ virtual screen to render on"""

        self.virtual_screen_size = (100, 100)
        """ size of the virtual screen to render on"""

        self.font = None
        """ font of the system """

        self.fontSize = 14
        """ size of the system font"""

        self.end = False
        """ interface loop end """

        self.root_path = self.config['root_path']
        """ root path of the application"""

        self.ui_manager = None
        """ pygame_gui manager instance"""

        self.ui_theme_file = None
        """ pygame_gui theme file"""

        self.resources = {}
        """ displaying resource """

        self.skip_observation = OmegaConf.select(self.config, 'interface.skip_observations', default=True)
        """ may some observations skipped?"""

        self.system_color = (255, 255, 0)
        """ system color for displaying information"""

        # environment related information
        if game_class_ is None or interface_role is None:
            raise CreationException('game_class_ and interface_role must not be None')

        self.interface_role = interface_role
        """ role of the interface. see @ConnectedSubAppInfo"""

        self.environment = pm.interface.EnvironmentInterface(id_env=self.id, cfg=self.config)
        """ environment interface"""

        self.environment.game = game_class_(cfg=cfg)
        self.controller_interface_class_ = None
        """ class of the controller used by the interface"""

        self.controller = None
        """ controller used by the interface"""

        self.last_step_choose_action = None
        """ last step the interface have chosen action"""

        # interface element related information
        self.console = None
        """ console UI """

        # debug related information
        self.interface_dbg_info_index = 0
        """ DEBUG information """
        self.debug_info_labels = []
        """ DEBUG labels"""
        self.fps = []
        """ DEBUG FPS information"""

        # client/server/engine related information
        self.engine_id = None
        """ connected engine id"""
        self.remote_engine_host = remote_engine_host
        """ host of the engine """
        self.remote_engine_port = remote_engine_port
        """ port of the engine """
        if search_remote or remote_engine_host is not None:
            self.remote_communication = Client(ident=self.id,
                                               host=remote_engine_host,
                                               port=remote_engine_port,
                                               socket_handler_class=SocketHandlerQueue,
                                               socket_handler_args=(self.messages_received,))
            if search_remote:
                self.remote_communication.search_server()
                if self.remote_communication.host is None or self.remote_communication.port is None:
                    raise ConnectionError('No server found for remote connection.')
            self.remote_communication.connect()

    def load_resources(self) -> None:
        """ Load the graphical resources """
        pass

    def init_graphics(self) -> None:
        """
        Init the graphical elements
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("dejavusansmono", self.fontSize)

        # Warning : pygame.SCALED slows down fps
        #flags = pygame.SCALED
        flags = 0
        # Keep 16:9 ratio (1368, 768) (1920, 1080) (2560, 1440)
        # https://www.sven.de/dpi/
        # https://developer.android.com/training/multiscreen/screendensities
        # https://benui.ca/unreal/ui-resolution/
        # https://blogs.windows.com/windowsdeveloper/2017/05/19/improving-high-dpi-experience-gdi-based-desktop-apps/
        screen_resolution = self.config.interface.get('resolution', [1368, 768])
        self.screen = pygame.display.set_mode(tuple(screen_resolution), flags=flags)
        self.virtual_screen = pygame.Surface(self.virtual_screen_size).convert_alpha()

        self.load_resources()

        self.ui_manager = UIManager(self.virtual_screen_size,
                                    theme_path=self.ui_theme_file)
        ratio_x = (self.virtual_screen.get_width() / self.screen.get_width())
        ratio_y = (self.virtual_screen.get_height() / self.screen.get_height())
        # undocumented pygame_gui feature... hope it will stay as is :)
        # see https://github.com/MyreMylar/pygame_gui/issues/210
        self.ui_manager.mouse_pos_scale_factor = [ratio_x, ratio_y]

        for k_gr in self.resources.keys():
            self.resources[k_gr] = self.resources[k_gr].convert_alpha(self.virtual_screen)

        console_size = (self.virtual_screen_size[0], self.virtual_screen_size[1] / 3)
        self.console = UIConsoleWindow(pygame.Rect((0, 0), console_size),
                                       manager=self.ui_manager,
                                       window_title='Console',
                                       object_id='#console',
                                       visible=False)
        self.console.change_layer(200)

        self.interface_dbg_info_index = self.add_debug_label()
        self.interface_dbg_queue_index = self.add_debug_label()

    def add_debug_label(self) -> int:
        """
        Adding a new graphical debug labels. A text can be set later to add debug info, displayed on the top of all.

        :return: The index of the new added label
        """
        pos_y = 0
        font_info = self.ui_manager.get_theme().get_font_info(["#fps_counter"])
        if self.debug_info_labels:
            pos_y = self.debug_info_labels[-1].get_relative_rect()[1] + int(int(font_info['size']) * 1.5)
        label = UILabel(pygame.Rect(0,
                                    pos_y,
                                    int(self.virtual_screen.get_width() * 3 / 4),
                                    int(int(font_info['size']) * 1.5)),
                        "",
                        self.ui_manager,
                        object_id='#fps_counter')

        label.change_layer(1000)
        label.hide()
        self.debug_info_labels.append(label)
        return len(self.debug_info_labels) - 1

    def init_game(self) -> None:
        """
        Initialize game : Connect to engine, define the game and register self as a new interface
        """
        if self.remote_communication is not None:
            self.engine_id = self.remote_communication.server_id
            self.register_connected_sub_app(sub_app_id=self.engine_id,
                                            role=ConnectedSubAppInfo.ROLE_SERVER,
                                            sent_q=None)
        else:
            self.engine_id = list(self.connected_sub_app.keys())[0]

        self.controller = self.controller_interface_class_(self.environment)

        init_message = Message(Message.MESSAGE_TYPE_DEFINE, {'game': self.environment.game.__class__}, self.id)
        self.send_message(init_message, self.engine_id)

        register_message = Message(Message.MESSAGE_TYPE_REGISTER,
                                   {'id': self.id,
                                    'queue_id': self.messages_received_q_id,
                                    'role': self.interface_role},
                                   self.id)
        self.send_message(register_message, self.engine_id)

    def receive_observation(self) -> None:
        """
        Wait for an OBSERVATION message (or END_GAME) from the engine and update the interface environment
        """
        obs_msg = self.wait_message([Message.MESSAGE_TYPE_OBSERVATION, Message.MESSAGE_TYPE_END_GAME],
                                    block=False,
                                    most_recent=self.skip_observation,
                                    keep_all=[Message.MESSAGE_TYPE_END_GAME])
        if obs_msg is not None:
            if obs_msg.msg_type == Message.MESSAGE_TYPE_OBSERVATION:
                observation_xml = obs_msg.params['observation']
                self.logger.debug('Observation received %s',LazyXMLString(observation_xml))

                additional_info = dict()
                if 'additional_information' in obs_msg.params:
                    additional_info = obs_msg.params['additional_information']
                    self.logger.debug('Additional info received %s', additional_info)
                    if 'log' in additional_info:
                        self.console.add_output_line_to_log(str(additional_info['log']))

                self.environment.update_current_next(observation_xml, additional_info)

                for ag in self.environment.agents:
                    if ag.control == self.id:
                        ag.controller = self.controller
                        self.environment.controlled_agent = ag
                self.messages_received.task_done()

                self.get_current_app_state().on_receive_observation()
            if obs_msg.msg_type == Message.MESSAGE_TYPE_END_GAME:
                self.logger.debug('End Game message received from Engine')
                self.end = True
        else:
            self.logger.debug('No observation received')

    def handle_event(self) -> None:
        """
        Handle interface events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_HASH:
                    if self.console.visible == 0:
                        self.console.show()
                    else:
                        self.console.hide()
                if event.key == K_d:
                    if event.mod & pygame.KMOD_CTRL:
                        for d in self.debug_info_labels:
                            if d.visible == 0:
                                d.show()
                            else:
                                d.hide()
                    if event.mod & pygame.KMOD_ALT:
                        self.ui_manager.set_visual_debug_mode(True)
                    else:
                        self.ui_manager.set_visual_debug_mode(False)

            self.ui_manager.process_events(event)
            self.get_current_app_state().handle_event(event)

    def choose_action(self) -> None:
        """
        Let the agent choose action if conditions are respected:
        - The interface is a ROLE_ACTOR
        - The interface has received a new observation since the agent's last action.
        """
        if self.interface_role == ConnectedSubAppInfo.ROLE_ACTOR:
            # last_step_choose_action is used to choose the (interface) step when an agent should choose an action
            # It occurs when the interface received a new observation
            if self.last_step_choose_action is None or self.last_step_choose_action < self.environment.current_step:
                self.environment.choose_action()
                if self.environment.controlled_agent is not None and self.environment.controlled_agent.action:
                    self.last_step_choose_action = self.environment.current_step

    def send_action(self) -> None:
        """
        Send the action chosen by the interface. Only if the interface is a ROLE_ACTOR
        """
        if self.interface_role == ConnectedSubAppInfo.ROLE_ACTOR:
            if self.environment.controlled_agent is not None:
                if self.environment.controlled_agent.action is not None:
                    act_msg = Message(msg_type=Message.MESSAGE_TYPE_ACTION,
                                      param_dict={'action': self.environment.controlled_agent.action},
                                      src_sub_app_id=self.id)
                    self.send_message(act_msg, self.engine_id)
                    self.logger.debug('Action sent %s',
                                      ElementTree.tostring(self.environment.controlled_agent.action.to_xml()))
                    # send the action only once
                    self.environment.controlled_agent.action = None

    def update(self) -> None:
        """ update the current app state """
        self.get_current_app_state().update()

    def display_text(self, text, position) -> None:
        """
        quick display of a text with system font.

        :param text: text to display
        :param position: position of the text
        """
        self.screen.blit(self.font.render(text, True, self.system_color), position)

    def render(self, time_delta) -> None:
        """
        Render the environment current state and other information on screen
        """
        self.virtual_screen.fill('black')
        if self.environment.current_state is not None:
            self.ui_manager.update(time_delta)
            self.get_current_app_state().render(time_delta)
            self.ui_manager.draw_ui(self.virtual_screen)
        self.screen.blit(pygame.transform.smoothscale(self.virtual_screen, self.screen.get_rect().size), (0, 0))
        #self.screen.blit(pygame.transform.scale(self.virtual_screen, self.screen.get_rect().size), (0, 0))
        # self.screen.blit(self.virtual_screen, (0, 0))

        if time_delta != 0:
            self.fps.append(1/time_delta)
            self.fps = self.fps[-100:]
            fps = sum(self.fps)/len(self.fps)
            mouse_pos = self.ui_manager.get_mouse_position()
            self.display_text(f'FPS: {fps:>3.0f} ({1 / time_delta:>3.2f})',
                              (self.screen.get_rect().size[0]-(self.fontSize*2)-200,
                               self.screen.get_rect().size[1]-(self.fontSize*2)))
            if self.debug_info_labels[self.interface_dbg_info_index].visible == 1:
                self.debug_info_labels[self.interface_dbg_info_index].set_text(f'Mouse pos : {str(pygame.mouse.get_pos())} '
                                                                               f'Mouse pygame_gui pos : {str(mouse_pos)}')
            if self.debug_info_labels[self.interface_dbg_queue_index].visible == 1:
                self.debug_info_labels[self.interface_dbg_queue_index].set_text(f'Interface queue size: {str(self.messages_received.qsize())}')

        pygame.display.update()

    def run(self) -> None:
        """
        Main interface loop
        """
        self.init_graphics()
        self.init_game()

        self.receive_observation()

        self.render(0.0)

        clock = pygame.time.Clock()
        self.end = False
        while not self.end:
            time_delta = clock.tick(60) / 1000
            self.handle_event()
            self.update()
            self.render(time_delta)

        msg_quit = Message(msg_type=Message.MESSAGE_TYPE_QUIT_GAME, param_dict=None, src_sub_app_id=self.id)
        self.send_message(msg_quit, self.engine_id)
        if self.remote_communication is not None:
            self.remote_communication.send_frame_to(self.engine_id, Frame.bye_frame())

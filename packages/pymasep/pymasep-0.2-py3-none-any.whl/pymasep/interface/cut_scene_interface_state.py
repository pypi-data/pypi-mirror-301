from pymasep.interface import Interface
from pymasep.interface.interface_state import InterfaceState
import pymasep.interface.user_event as user_event
import cv2
import pygame
import pygame_gui
from pygame.locals import *


class CutSceneInterfaceState(InterfaceState):
    """
    Interface state to handle a cut scene with video

    EXPERIMENTAL: because of performance issues, caused by cv2 random access video, only small video (small resolution and/or old format) are fully supported
    Otherwise, the video will be displayed, but the user event would be delayed/not handled during video playing.
    Wait for the pygame sdl video support.

    Helped from https://www.reddit.com/r/pygame/comments/12kl1m6/playing_video_and_sound_simultaneously/#
    and https://forum.opencv.org/t/cap-set-cv2-cap-prop-pos-msec-changes-to-unreachable-timestamp/6561.
    Thanks!
    """

    def __init__(self, sub_application: Interface, video_path: str, audio_path: str, scene_name: str ):
        """
        :param sub_application: the interface to display the video on
        :param video_path: the path to the video file
        :param audio_path: the path to the audio file
        :scene_name: the name of the game phase when the video is played
        """
        super().__init__(sub_application, sub_application.virtual_screen_size)
        self.video_path = video_path
        """ the path to the video file"""

        self.audio_path = audio_path
        """ the path to the audio file"""

        self.scene_name = scene_name
        """ the name of the game phase when the video is played"""

        self.video = None
        """ the video object"""

        self.ended = False
        """ the video has finished"""

        self.current_ts = 0
        """ current timestamp of the video"""

        self.image = None
        """ image used to display the video """


    def init(self)->None:
        super().init()
        self.video = cv2.VideoCapture(self.video_path)
        pygame.mixer.music.load(self.audio_path)  # Should be the same file (movie and audio)
        self.image = pygame_gui.elements.UIImage(relative_rect=self.sub_application.virtual_screen.get_rect(),
                                                 manager=self.sub_application.ui_manager,
                                                 container=self.ui_container,
                                                 image_surface=pygame.Surface((1, 1)))

    def clean(self) -> None:
        super().clean()
        pygame.mixer.music.stop()

    def handle_event(self, event) -> None:
        """
        Handle events to close the cut scene
        :param event: the event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                evt_end = pygame.event.Event(user_event.VIDEO_ENDED_EVENT)
                pygame.event.post(evt_end)

        self.sub_application.environment.controlled_agent.controller.select_action(event)

    def render(self, time_delta) -> None:
        """
        Render the cut scene

        :param time_delta: The time delta since the last call
        """
        if self.current_ts == 0:
            pygame.mixer.music.play()
        self.current_ts += time_delta
        self.video.set(cv2.CAP_PROP_POS_MSEC, float(self.current_ts*1000))
        success, video_image = self.video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            self.image.set_image(video_surf)
        else:
            self.ended = True

    def update(self) -> None:
        super().update()
        if self.ended:
            evt_end = pygame.event.Event(user_event.VIDEO_ENDED_EVENT)
            pygame.event.post(evt_end)
        current_state = self.sub_application.environment.current_state
        game = self.sub_application.environment.game
        if current_state is not None and game.get_system_value(current_state, 'GamePhase') != self.scene_name:
            self.sub_application.pop_state()

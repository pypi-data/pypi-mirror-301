from typing import Type
from queue import Queue
import os

from omegaconf import DictConfig, OmegaConf

from pymasep.interface.interface import Interface
from pymasep.engine.engine import Engine
from pymasep.application.connected_sub_app_info import ConnectedSubAppInfo


class App:
    """
    Main application class.
    """

    LAUNCH_ALL_LOCAL = 0
    """ Launch threaded server and interface """

    LAUNCH_INTERFACE = 1
    """ Launch only interface (remote) """

    LAUNCH_SERVER_STANDALONE = 2
    """ Launch only server (remote) """

    def __init__(self,
                 interface_class_: Type[Interface],
                 root_path: str = '.',
                 config_path: str = 'config',
                 launch: int = LAUNCH_ALL_LOCAL,
                 remote_engine_host: str = None,
                 remote_engine_port: int = None):
        """
        :param interface_class_: class of the interface
        :param root_path: path of the application root directory. Used for testing and packaging
        :param config_path: path of the config files, relative to the root_path
        :param launch: Type of launch (local, interface only, server only)
        :param remote_engine_host: engine host for remote interface. Maybe None for local and server only
        :param remote_engine_port: engine port for remote interface. Maybe None for local and server only
        """
        self.engine = None
        """ engine sub application """

        self.interface = None
        """ interface sub application """

        self.queues = [Queue()]
        """ queues used to communicate between engine and interface"""

        interface_queue_id = 0
        engine_queue_id = 0
        max_connection = 10

        self.root_path = root_path
        """ root path of the application"""

        self.config = App.load_config(os.path.join(self.root_path, config_path))
        """ config of the application"""

        self.config['root_path'] = self.root_path

        if launch == App.LAUNCH_ALL_LOCAL:
            self.queues.append(Queue())
            interface_queue_id = 1
        if launch != App.LAUNCH_INTERFACE:  # LAUNCH_ALL_LOCAL or LAUNCH_SERVER_STANDALONE
            self.engine = Engine(app=self, received_q_id=engine_queue_id,
                                 cfg=self.config,
                                 max_connection=max_connection)
        if launch != App.LAUNCH_SERVER_STANDALONE:  # LAUNCH_ALL_LOCAL or LAUNCH_INTERFACE
            self.interface_class_: Type[Interface] = interface_class_
            search_remote = ((remote_engine_host is None or remote_engine_port is None)
                             and launch == App.LAUNCH_INTERFACE)
            self.interface = self.interface_class_(app=self,
                                                   received_q_id=interface_queue_id,
                                                   cfg=self.config,
                                                   remote_engine_host=remote_engine_host,
                                                   remote_engine_port=remote_engine_port,
                                                   search_remote=search_remote)
        if launch == App.LAUNCH_ALL_LOCAL:
            self.interface.register_connected_sub_app(self.engine.id,
                                                      ConnectedSubAppInfo.ROLE_SERVER,
                                                      self.queues[engine_queue_id])

    @staticmethod
    def load_config(config_path) -> DictConfig:
        """
        Load config from a path. Load app.yaml file.

        :param config_path: Path of the configuration files
        :return: OmegaConf Configuration
        """
        config = OmegaConf.load(os.path.join(config_path, 'app.yaml'))
        return config

    def run(self):
        """
        Run the application. Launch Engine, Interface or both. Wait for termination.
        """
        if self.engine:
            self.engine.start()
        if self.interface:
            self.interface.start()
        if self.engine:
            self.engine.join()
        if self.interface:
            self.interface.join()

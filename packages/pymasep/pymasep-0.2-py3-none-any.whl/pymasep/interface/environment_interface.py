from xml.etree.ElementTree import Element
from omegaconf import DictConfig

from pymasep.common.environment import Environment


class EnvironmentInterface(Environment):
    """
    Represents the environment of the game (Interface part). This object keeps all dynamic value of the game.
    This environment chooses the action of the agent controlled by the interface.
    """

    def __init__(self, id_env: str = None, cfg: DictConfig = None) -> None:
        super().__init__(id_env=id_env, cfg=cfg)

        self.controlled_agent = None
        """ the agent controlled by the interface"""

    def choose_action(self) -> None:
        """
        tell the agent controlled by interface to choose their action
        """
        if self.controlled_agent is not None:
            self.controlled_agent.choose_action()
            if self.controlled_agent.action:
                self.logger.debug('choose_action() %s %s', self.controlled_agent.name, self.controlled_agent.action)
            else:
                self.logger.debug('choose_action() %s None', self.controlled_agent.name)

    def update_current_next(self, observation_xml: Element, additional_info) -> None:
        """
        update the current state of the interface from the observation

        :param observation_xml: observation as XML
        :param additional_info: additional information
        """
        self.clear_all_state_elements()
        self.current_state = self.create_object(xml_node=observation_xml, parent=None)
        self.current_step = self.current_state.step
        self.current_additional_info = additional_info
        self.logger.debug('State : %s', self.current_state)
        self.logger.debug('Additional info : %s', self.current_additional_info)

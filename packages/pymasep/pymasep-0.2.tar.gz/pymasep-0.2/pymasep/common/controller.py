from typing import Optional, Any


class Controller:
    """
    Abstract controller to control an agent in the environment
    """

    def __init__(self, environment) -> None:
        """
        :param environment: environment for the controller
        """
        self.environment = environment

    def action_choice(self, observation, agent):
        """
        Choose the action.

        :param pymasep.common.State observation: The observation used to choose the action.
        :param pymasep.common.Agent agent: The agent who chooses the action.
        :return: The action (pymasep.common.Action) chose for the agent.
        """
        pass

    def on_observe(self, observation, reward: Optional[Any] = None):
        """
        Do something when the agent observes the state and possibly a reward.

        Useful for learning controllers.

        :param pymasep.common.State observation: The observation used to choose the action.
        :param reward: The reward obtained.
        """
        pass

from abc import ABC, abstractmethod
# Note this is a needed duplicate of BasePlayer.py in the PROJECT_ROOT/players/ directory

class Player(ABC):
    """
    Abstract base class representing a generic player in the environment.
    All specific player implementations (e.g., RL, GA, scripted) should inherit from this.
    """

    def __init__(self, name="Player"):
        """
        Initialize the player with a given name.
        """
        self.name = name

    @abstractmethod
    def get_action(self, state):
        """
        Abstract method to decide an action given the current state.
        Must be implemented by subclasses.
        """
        pass

    def remember(self, *args):
        """
        Store experience for training (optional override).
        Used in learning agents to collect data for training.
        """
        pass

    def train(self):
        """
        Train the model based on stored experiences (optional override).
        """
        pass

    def reset(self):
        """
        Reset internal state at the end of an episode (optional override).
        """
        pass

    def can_train(self):
        """
        Indicates whether this player supports training.
        Returns False by default; should be overridden if applicable.
        """
        return False

    def can_evolve(self):
        """
        Indicates whether this player supports evolutionary updates.
        Returns False by default; should be overridden if applicable.
        """
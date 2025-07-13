from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name="Player"):
        self.name = name

    @abstractmethod
    def get_action(self, state):
        pass

    def remember(self, *args):
        pass

    def train(self):
        pass

    def reset(self):
        pass

    def can_train(self):
        return False

    def can_evolve(self):
        return False
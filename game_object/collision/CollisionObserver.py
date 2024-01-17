from abc import ABC, abstractmethod

class CollisionObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def on_collide(self, observer) -> None:
        """
        Receive update from subject.
        """
        pass

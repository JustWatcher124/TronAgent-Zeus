from abc import ABC, abstractmethod
from game_object.collision.CollisionSubject import CollisionSubject

class CollisionObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def on_collide(self, subject: CollisionSubject) -> None:
        """
        Receive update from subject.
        """
        pass

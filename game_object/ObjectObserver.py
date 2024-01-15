from abc import ABC, abstractmethod

class ObjectObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self) -> None:
        """
        Receive update from subject.
        """
        pass

from game_object.collision.CollisionObserver import CollisionObserver
from game_object.collision.CollisionSubject import CollisionSubject


class CollisionManger(CollisionSubject):

    _state: int = 1
    _observers: list[CollisionObserver] = []

    def attach(self, observer: CollisionObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: CollisionObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.on_collide(self)


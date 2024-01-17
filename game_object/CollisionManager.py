from typing import List
from game_object.base.GameObject import GameObject
from singleton.SingletonMeta import SingletonMeta


class CollisionManger(metaclass=SingletonMeta):

    _observers: List[GameObject]

    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: GameObject) -> None:
        self._observers.append(observer)

    def detach(self, observer: GameObject) -> None:
        self._observers.remove(observer)


    ### POTENTIAL PERFORMANCE BOTTLENECK
    def check_for_collisions(self) -> None:
        for observer in self._observers:
            for observer_collided_with in self._observers:
                if not observer is observer_collided_with:
                    if observer.position == observer_collided_with.position:
                        observer.on_collide(observer_collided_with)
                



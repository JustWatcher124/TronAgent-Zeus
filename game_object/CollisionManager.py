from typing import List
from game_object.base.GameObject import GameObject
from position import Position
from singleton.SingletonMeta import SingletonMeta


class CollisionManger(metaclass=SingletonMeta):

    _observers: List[GameObject]

    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: GameObject) -> None:
        self._observers.append(observer)

    def detach(self, observer: GameObject) -> None:
        self._observers.remove(observer)

    def reset(self) -> None:
        self._observers = []

    ### POTENTIAL PERFORMANCE BOTTLENECK
    def check_for_collisions(self) -> None:
        for observer in self._observers:
            for observer_collided_with in self._observers:
                if not observer is observer_collided_with:
                    if observer.position == observer_collided_with.position:
                        observer.on_collide(observer_collided_with)

    def will_be_collision(self, position: Position) -> bool:
        for observer in self._observers:
            if position == observer.position:
                return True
        return False
                
## API
collision_manager = CollisionManger()

def AttachCollider(game_object: GameObject) -> None:
    collision_manager.attach(game_object)

def WillBeACollision(position: Position) -> bool:
    return collision_manager.will_be_collision(position)

def CheckForCollision() -> None:
    collision_manager.check_for_collisions()

def ResetCollisionManager() -> None:
    collision_manager.reset()
    





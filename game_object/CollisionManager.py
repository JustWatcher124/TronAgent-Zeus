from typing import List, Tuple
from game_object.base.GameObject import GameObject
from position import Position
from settings import BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from singleton.SingletonMeta import SingletonMeta


class CollisionManger(metaclass=SingletonMeta):

    _observers: List[GameObject]
    _last_observers_state: List[GameObject]
    _center: Position

    def __init__(self) -> None:
        self._observers = []
        self._last_observers_state = []
        self._center = Position((SCREEN_WIDTH / 2) - BLOCK_SIZE, (SCREEN_HEIGHT / 2) - BLOCK_SIZE)

    def _attach(self, observer: GameObject) -> None:
        self._observers.append(observer)

    def _detach(self, observer: GameObject) -> None:
        self._observers.remove(observer)

    def _reset(self) -> None:
        self._observers = []

    def _sort_observers(self, game_object: GameObject):
        return game_object.name

    ### POTENTIAL PERFORMANCE BOTTLENECK
    def _check_for_collisions(self) -> None:
        changed: List[GameObject] = []

        if len(self._last_observers_state) == 0:
            self._last_observers_state = self._observers

        self._observers.sort(key=self._sort_observers)
        self._last_observers_state.sort(key=self._sort_observers)

        for idx, observer in enumerate(self._observers):
            if observer.position != self._last_observers_state[idx]:
                changed.append(observer)

        for observer in changed:
            for observer_collided_with in self._observers:
                if not observer is observer_collided_with:
                    if observer.position == observer_collided_with.position:
                        observer.on_collide(observer_collided_with)
        
        self._last_observers_state = self._observers

    def _will_be_collision(self, position: Position) -> bool:
        for observer in self._observers:
            if position == observer.position:
                return True
        return False

    def _is_collide(self, game_object: GameObject) -> bool:
        for observer in self._observers:
            if game_object.position == observer.position and not game_object is observer:
                return True
        return False

                
## API
collision_manager = CollisionManger()

def AttachCollider(game_object: GameObject) -> None:
    collision_manager._attach(game_object)

def WillBeACollision(position: Position) -> bool:
    return collision_manager._will_be_collision(position)

def CheckForCollision() -> None:
    collision_manager._check_for_collisions()

def ResetCollisionManager() -> None:
    collision_manager._reset()

def IsCollide(game_object: GameObject) -> bool:
    return collision_manager._is_collide(game_object)
    





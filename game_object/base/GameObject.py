from typing import Tuple
from game_object.ObjectObserver import ObjectObserver
from game_object.collision.CollisionObserver import CollisionObserver
from position import Position

class GameObject(CollisionObserver, ObjectObserver):
    position: Position
    color: Tuple
    name: str
    
    def __init__(self, position: Position, name: str, color: Tuple) -> None:
        super().__init__()
        self.position = position
        self.name = name
        self.color = color

    def init(self) -> None:
        pass

    def update(self) -> None:
        pass

    def on_collide(self, observer) -> None:
        print("Collide!", observer.name)
        pass

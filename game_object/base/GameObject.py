from pygame import Color
from game_object.ObjectObserver import ObjectObserver
from game_object.collision.CollisionObserver import CollisionObserver
from game_object.collision.CollisionSubject import CollisionSubject
from position import Position

class GameObject(CollisionObserver, ObjectObserver):
    position: Position
    color: Color
    name: str
    
    def __init__(self, position: Position, name: str, color: Color) -> None:
        super().__init__()
        self.position = position
        self.name = name
        self.color = color

    def init(self) -> None:
        pass

    def update(self) -> None:
        print("Hello")

    def on_collide(self, subject: CollisionSubject) -> None:
        pass

from game_object.base.GameObject import GameObject
from pygame import Color
from game_object.collision.CollisionSubject import CollisionSubject
from position import Position

class LightCycleTail(GameObject):

    def __init__(self, position: Position, name: str, color: Color) -> None:
        super().__init__(position, name, color)

    def on_collide(self, subject: CollisionSubject) -> None:
        pass

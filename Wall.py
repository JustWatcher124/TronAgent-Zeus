from pygame import Color
from game_object.base.GameObject import GameObject
from position import Position


class Wall(GameObject):

    def __init__(self, position: Position, name: str, color: Color) -> None:
        super().__init__(position, name, color)

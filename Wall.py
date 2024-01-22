from typing import Tuple
from game_object.CollisionManager import AttachCollider, CollisionManger
from game_object.base.GameObject import GameObject
from position import Position


class Wall(GameObject):

    def __init__(self, position: Position, name: str, color: Tuple) -> None:
        super().__init__(position, name, color)

        AttachCollider(self)

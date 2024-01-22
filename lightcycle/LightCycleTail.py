from typing import Tuple
from game_object.CollisionManager import AttachCollider
from game_object.base.GameObject import GameObject
from position import Position

class LightCycleTail(GameObject):

    def __init__(self, position: Position, name: str, color: Tuple, driver) -> None:
        super().__init__(position, name, color)
        
        self._driver = driver
        # Attach collider
        AttachCollider(self)

    def on_collide(self, observer: GameObject) -> None:
        self._driver.wins()

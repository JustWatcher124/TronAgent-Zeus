from typing import Tuple
from game_object.CollisionManager import CollisionManger
from game_object.base.GameObject import GameObject
from game_object.collision.CollisionSubject import CollisionSubject
from position import Position

class LightCycleTail(GameObject):

    def __init__(self, position: Position, name: str, color: Tuple) -> None:
        super().__init__(position, name, color)
        
        # Attach collider
        collision_manager = CollisionManger()
        collision_manager.attach(self)

    def on_collide(self, observer: GameObject) -> None:
        pass

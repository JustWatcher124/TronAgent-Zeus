from pygame import Color
from game_object.base.GameObject import GameObject
from game_object.collision.CollisionSubject import CollisionSubject
from lightcycle.LightCycleController import LightCycleController
from position import Position

class LightCycleHead(GameObject):
    _controller: LightCycleController

    def __init__(self, position: Position, name: str, color: Color) -> None:
        super().__init__(position, name, color)
        self._controller = LightCycleController(position)

    def update(self) -> None:
        self.position = self._controller.get_position()

    def on_collide(self, subject: CollisionSubject) -> None:
        pass


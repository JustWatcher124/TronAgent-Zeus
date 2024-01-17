from typing import Tuple
from game_object.CollisionManager import CollisionManger
from game_object.ObjectManager import ObjectManager
from game_object.base.GameObject import GameObject
from lightcycle.LightCycleController import LightCycleController
from lightcycle.LightCycleTail import LightCycleTail
from position import Position

class LightCycleHead(GameObject):
    _controller: LightCycleController

    def __init__(self, position: Position, name: str, color: Tuple, tail_color: Tuple) -> None:
        super().__init__(position, name, color)
        self._controller = LightCycleController(position)
        collision_manager = CollisionManger()
        collision_manager.attach(self)
        self._object_manager = ObjectManager()
        self.tail_length = 0
        self.tail_color = tail_color

    def update(self) -> None:
        last_position = self.position
        self.position = self._controller.get_position()
        self.spawn_tail(last_position)


    def on_collide(self, observer: GameObject) -> None:
        print("my name is", self.name, "and I collided with", observer.name)

    def spawn_tail(self, position: Position):

        self._object_manager.attach(
            LightCycleTail(
                position,
                str(self.tail_length),
                self.tail_color
            )
        )

        self.tail_length += 1

from typing import Tuple
from InstantiateGameObject import InstantiateGameObject
from ResetGame import ResetGame
from game_object.CollisionManager import CollisionManger
from game_object.base.GameObject import GameObject
from lightcycle.LightCycleController import LightCycleController
from lightcycle.LightCycleTail import LightCycleTail
from position import Position

class LightCycleHead(GameObject):
    _controller: LightCycleController

    def __init__(self, position: Position, name: str, color: Tuple, tail_color: Tuple) -> None:
        super().__init__(position, name, color)
        self._controller = LightCycleController(position)
        
        # Attach collider
        collision_manager = CollisionManger()
        collision_manager.attach(self)

        self.tail_length = 0
        self.tail_color = tail_color

    def update(self) -> None:
        last_position = self.position
        self.position = self._controller.get_position()
        self._spawn_tail(last_position)


    def on_collide(self, observer: GameObject) -> None:
        print("my name is", self.name, "and I collided with", observer.name)
        ResetGame()


    def _spawn_tail(self, position: Position):

        InstantiateGameObject(
            LightCycleTail(
                position,
                f"{self.name}_tail_{self.tail_length}",
                self.tail_color
            )
        )

        self.tail_length += 1

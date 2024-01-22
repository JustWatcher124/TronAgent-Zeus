from typing import Tuple
from ResetGame import ResetGame
from game_object.CollisionManager import AttachCollider, IsCollide
from game_object.ObjectManager import InstantiateObject
from game_object.base.GameObject import GameObject
from lightcycle.LightCycleTail import LightCycleTail
from ml.MLController import MLController
from position import Position
from settings import DEBUG

class LightCycleHead(GameObject):
    _controller: MLController
    _did_collide: bool
    _did_win: bool

    def __init__(self, position: Position, name: str, color: Tuple, tail_color: Tuple) -> None:
        super().__init__(position, name, color)
        self._controller = MLController(position)
        
        AttachCollider(self)
        self._did_collide = False
        self.tail_length = 0
        self.tail_color = tail_color
        self._did_win = False

    def update(self) -> None:
        last_position = self.position
        self.position = self._controller.get_position()
        if IsCollide(self):
            self._controller.set_reward(-10)
            self._controller.set_done(True)
            self._did_collide = True
        self._spawn_tail(last_position)
        self._controller.train() 
        if DEBUG:
            print("")
            print("last state:", self._controller._last_state, "state:", self._controller._state, "reward:", self._controller._reward)

    def wins(self) -> None:
        self._did_win = True

    def on_collide(self, observer: GameObject) -> None:
        self._did_collide = True

    def _did_collide_seq(self):
        self._controller.set_reward(-10)
        self._controller.set_done(True)
        self._controller.train()
        ResetGame()

    def _spawn_tail(self, position: Position) -> None:

        InstantiateObject(
            LightCycleTail(
                position,
                f"{self.name}_tail_{self.tail_length}",
                self.tail_color,
                driver=self
            )
        )

        self.tail_length += 1

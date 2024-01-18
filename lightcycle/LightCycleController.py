from enum import Enum
from PygameEvents import PygameEvents
from game_object.CollisionManager import WillBeACollision
from position import Position
from settings import BLOCK_SIZE
import numpy as np

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class LightCycleController:
    _x: int
    _y: int
    _direction: Direction
    _pygame_events: PygameEvents

    def __init__(self, starting_position: Position) -> None:
        self._x = starting_position.x
        self._y = starting_position.y
        self._pygame_events = PygameEvents()
        self._direction = Direction.UP
        
    def _get_dir(self) -> None:
        up = Position(self._x, self._y + BLOCK_SIZE)
        down = Position(self._x, self._y - BLOCK_SIZE)
        left = Position(self._x - BLOCK_SIZE, self._y)
        right = Position(self._x + BLOCK_SIZE, self._y)
        
        dirs = [
            (Direction.UP, WillBeACollision(up)),
            (Direction.DOWN, WillBeACollision(down)),
            (Direction.LEFT, WillBeACollision(left)),
            (Direction.RIGHT, WillBeACollision(right)),
        ]
        
        possible_dirs = []

        for dir in dirs:
            if dir[1] != True:
                possible_dirs.append(dir[0])
        
        if self._direction in possible_dirs:
            return
        
        

    def get_position(self) -> Position:
        self._get_dir()
        if self._direction == Direction.RIGHT:
            self._x += BLOCK_SIZE
        elif self._direction == Direction.LEFT:
            self._x -= BLOCK_SIZE
        elif self._direction == Direction.DOWN:
            self._y += BLOCK_SIZE
        elif self._direction == Direction.UP:
            self._y -= BLOCK_SIZE
        
        return Position(self._x, self._y)

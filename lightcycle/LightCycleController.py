from PygameEvents import PygameEvents
from game_object.CollisionManager import WillBeACollision
from position import Position
from settings import BLOCK_SIZE
from Direction import Direction
import numpy as np

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
        up = Position(self._x, self._y - BLOCK_SIZE)
        down = Position(self._x, self._y + BLOCK_SIZE)
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
            rand = np.random.rand()
            if rand < 0.05 and len(possible_dirs) > 1:
                self._direction = possible_dirs[np.random.randint(0, len(possible_dirs) - 1)]
            elif len(possible_dirs) < 1:
                self._direction = possible_dirs[0]
            return
        
        rand = np.random.rand()
        if len(possible_dirs) == 0:
            return
        elif len(possible_dirs) == 1:
            self._direction = possible_dirs[0]
        elif rand > 0.5:
            self._direction = possible_dirs[0]
        else:
            self._direction = possible_dirs[1]
        

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

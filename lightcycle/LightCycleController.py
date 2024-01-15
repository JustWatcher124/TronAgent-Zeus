from enum import Enum
import pygame
from PygameEvents import PygameEvents
from position import Position
from settings import BLOCK_SIZE

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
        
    def _get_dir(self):
        for event in self._pygame_events.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                   self._direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                   self._direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                   self._direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                   self._direction = Direction.DOWN

    def get_position(self):
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

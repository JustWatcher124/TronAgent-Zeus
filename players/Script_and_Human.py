from collections import deque
from settings import *
import pygame
from position import Position
from direction import Direction
from .BasePlayer import Player
import numpy as np
import random



class HumanPlayer(Player):
    """
    Human-controlled player using keyboard input (LEFT/RIGHT arrows)
    Info: With High Framerates this becomes essentially unplayable.
    """
    def __init__(self, name="You"):
        super().__init__(name)

    def get_action(self, state, position: Position, _):
        """
        Returns an action based on current keyboard state.
        """
        keys = pygame.key.get_pressed()

        
        action = [1, 0, 0]  # default: go straight

        if keys[pygame.K_RIGHT]:
            action = [0, 1, 0]  # turn right
        elif keys[pygame.K_LEFT]:
            action = [0, 0, 1]  # turn left

        return action


class ScriptedPlayer(Player):
    """
    Basic scripted player that always moves forward.
    """
    def __init__(self, name="ForwardBot"):
        super().__init__(name)

    def get_action(self, state, position: Position, _):
        """
        Always moves forward.
        """
        return [1, 0, 0]  # always forward


class ScriptedPlayerV2(Player):
    """
    Scripted player that dodges obstacles by turning randomly when blocked.
    """
    def __init__(self, name="Dodger", direction='right'):
        super().__init__(name)
        if direction == 'right':
            self.direction = Direction.RIGHT
        elif direction == 'left':
            self.direction = Direction.LEFT

    def get_action(self, state, position: Position, direction: Direction):
        """
        If obstacle is ahead, turns randomly left or right. Otherwise, moves forward.
        """
        x, y = position.x, position.y
        height, width = state.shape
        ahead = self._get_relative_position(position, direction)
        
        if not self._is_inside(ahead, width, height) or state[ahead.y, ahead.x] != 0:
            if random.random() > 0.5:
                action = [0, 1, 0]
            else:
                action = [0, 0, 1]
        else:
            action = [1, 0, 0]

        return action
    def _get_relative_position(self, pos, direction):  # helper function for the collision avoidance
        if direction == Direction.RIGHT:
            return Position(pos.x + 1, pos.y)
        elif direction == Direction.LEFT:
            return Position(pos.x - 1, pos.y)
        elif direction == Direction.UP:
            return Position(pos.x, pos.y - 1)
        elif direction == Direction.DOWN:
            return Position(pos.x, pos.y + 1)

    def _is_inside(self, pos, width, height):
        return 0 <= pos.x < width and 0 <= pos.y < height

    def _turn_right(self, direction):
        order = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        return order[(order.index(direction) + 1) % 4]

    def _turn_left(self, direction):
        order = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        return order[(order.index(direction) - 1) % 4]
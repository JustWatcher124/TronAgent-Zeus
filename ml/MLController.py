from typing import List
import torch
from PygameEvents import PygameEvents
from Direction import Direction
from ResetGame import ResetGame
from game_object.CollisionManager import WillBeACollision
from ml.Trainer import QTrainer
from ml.Model import Linear_QNet
from position import Position
from settings import BLOCK_SIZE
import numpy as np


class MLController():
    _x: int
    _y: int
    _direction: Direction
    _pygame_events: PygameEvents
    _qtrainer: QTrainer
    _model: Linear_QNet
    _epsilon: float
    _epsilon_decay: float
    _min_epsilon: float
    _action: List[int]
    _last_state: List[int]
    _state: List[int]
    _done: bool
    _n_games: int

    def __init__(self, starting_position: Position) -> None:
        self._x = starting_position.x
        self._y = starting_position.y
        self._pygame_events = PygameEvents()
        self._direction = Direction.UP
        self._model = Linear_QNet(8, 128, 3)
        self._qtrainer = QTrainer(self._model, 0.01, 0.995)
        self._epsilon = 0.995
        self._epsilon_decay = 0.01
        self._min_epsilon = 0.05
        self._action = [0, 0, 0]
        self._last_state = [0, 0, 0, 0, 0, 0, 0, 0]
        self._state = [0, 0, 0, 0, 0, 0, 0, 0]
        self._reward = 0
        self._done = False
        self._n_games = 0


    def _update_epsilon(self) -> None:
        print("eps",self._epsilon)
        if self._epsilon < self._min_epsilon:
            self._epsilon = self._min_epsilon
        elif self._epsilon > self._min_epsilon:
            self._epsilon *= self._epsilon_decay
        else:
            pass
        
    def _move(self) -> None:
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self._direction)

        if np.array_equal(self._action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(self._action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self._direction = new_dir

        if self._direction == Direction.RIGHT:
            self._x += BLOCK_SIZE
        elif self._direction == Direction.LEFT:
            self._x -= BLOCK_SIZE
        elif self._direction == Direction.DOWN:
            self._y += BLOCK_SIZE
        elif self._direction == Direction.UP:
            self._y -= BLOCK_SIZE

    def train(self) -> None:
        print("training")
        self._get_state()
        self._qtrainer.train_step(self._last_state, self._action, self._reward, self._state, self._done)
        self._qtrainer.remember(self._last_state, self._action, self._reward, self._state, self._done)
        if self._done:
            print("training long")
            self._qtrainer.train_long_memory()
            ResetGame()


    def set_reward(self, reward: int):
        self._reward = reward

    def set_done(self, done: bool):
        self._done = done

    def _get_state(self):
        self._last_state = self._state

        # the vision grid
        top_left = Position(self._x - BLOCK_SIZE, self._y - BLOCK_SIZE)
        up = Position(self._x, self._y - BLOCK_SIZE)
        top_right = Position(self._x + BLOCK_SIZE, self._y - BLOCK_SIZE)
        left = Position(self._x - BLOCK_SIZE, self._y)
        right = Position(self._x + BLOCK_SIZE, self._y)
        down = Position(self._x, self._y + BLOCK_SIZE)
        bottom_right = Position(self._x - BLOCK_SIZE, self._y + BLOCK_SIZE)
        bottom_left = Position(self._x + BLOCK_SIZE, self._y + BLOCK_SIZE)

        state: List[int] = [
            int(WillBeACollision(top_left)),
            int(WillBeACollision(up)),
            int(WillBeACollision(top_right)),
            int(WillBeACollision(left)),
            int(WillBeACollision(right)),
            int(WillBeACollision(bottom_left)),
            int(WillBeACollision(down)),
            int(WillBeACollision(bottom_right)),
        ] 
        
        self._state = state

    def _get_action(self):
        final_move = [0, 0, 0]
        if np.random.rand() < self._epsilon:
            move = np.random.randint(0, 2)
            final_move[move] = 1
        else:
            state_0 = torch.tensor(self._state, dtype=torch.float)
            predication = self._model(state_0)
            move = int(torch.argmax(predication).item())
            final_move[move] = 1

        self._action = final_move


    def get_position(self) -> Position:
        self._n_games += 1
        print("n_games", self._n_games)
        self._update_epsilon()
        self._get_state()
        self._get_action()
        self._move()
        return Position(self._x, self._y)

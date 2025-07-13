from model import Linear_QNet, QTrainer
from settings import *
from position import Position
from direction import Direction
from .BasePlayer import Player
from collections import deque
import torch
import numpy as np
import random

from model import Linear_QNet, QTrainer
from settings import *
from position import Position
from .BasePlayer import Player
from collections import deque
import torch
import numpy as np
import random

from model import Linear_QNet, QTrainer
from settings import *
from position import Position
from .BasePlayer import Player
from collections import deque
import torch
import numpy as np
import random
import math

class RLPlayer(Player):
    def __init__(self, name="RLAgent", input_size=25, subgrid_size=5):
        super().__init__(name)
        self.input_size = input_size
        self.model = Linear_QNet(self.input_size, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=GAMMA)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.epsilon = MIN_EPSILON
        self.n_games = 0

        self.subgrid_size = subgrid_size

    def _extract_state(self, grid, head: Position):
        if self.subgrid_size is None:
            return grid.flatten()
        if self.subgrid_size ** 2 != self.input_size:
            raise ValueError(f"Mismatch between subgrid_size={self.subgrid_size} and input_size={self.input_size}. subgrid_size needs to be the square root of input_size")
        half = self.subgrid_size // 2
        h, w = grid.shape
        cx, cy = head.x, head.y

        # Calculate bounds of the desired subgrid
        x_start = cx - half
        x_end = cx + half + 1
        y_start = cy - half
        y_end = cy + half + 1

        # Create empty grid with padding value (e.g., 5)
        padded_grid = np.full((self.subgrid_size, self.subgrid_size), fill_value=5, dtype=grid.dtype)

        # Compute actual indices to copy from original grid
        src_x_start = max(0, x_start)
        src_x_end = min(w, x_end)
        src_y_start = max(0, y_start)
        src_y_end = min(h, y_end)

        dst_x_start = src_x_start - x_start
        dst_x_end = dst_x_start + (src_x_end - src_x_start)
        dst_y_start = src_y_start - y_start
        dst_y_end = dst_y_start + (src_y_end - src_y_start)

        # Copy valid region into padded grid
        padded_grid[dst_y_start:dst_y_end, dst_x_start:dst_x_end] = grid[src_y_start:src_y_end, src_x_start:src_x_end]

        return padded_grid.flatten()
        

    def get_action(self, grid, head: Position, _):
        state = self._extract_state(grid, head)
        final_move = [0, 0, 0]
        if np.random.rand() < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        final_move[move] = 1
        # print(len(self.memory))
        return final_move

    def remember(self, state, head, next_head, action, reward, next_state, done):
        _state = self._extract_state(state, head)
        _next_state = self._extract_state(next_state, next_head)
        self.memory.append((_state, action, reward, _next_state, done))

    def train(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        try:
            self.trainer.train_step(states, actions, rewards, next_states, dones)
        except ValueError:
            print(self.name, 'states', set([state.shape for state in states]))
            print(self.name, 'next_states', set([state.shape for state in next_states]))
    def train_short(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * EPSILON_DECAY, MIN_EPSILON)

    def reset(self):
        self.n_games += 1
        self.decay_epsilon()

    def can_train(self):
        return True
    
    def save_model(self, episode, file_name=None):
        if file_name is None:
            file_name = f"{self.name}_input{self.input_size}_episode{episode}.pth"
        # file_name += f''
        self.model.save(file_name)

from model import Linear_QNet, QTrainer
from settings import *
from position import Position
from direction import Direction
from .BasePlayer import Player
from collections import deque
import torch
import numpy as np
import random

class RLPlayer(Player):
    def __init__(self, name="RLAgent"):
        super().__init__(name)
        self.model = Linear_QNet(25, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=GAMMA)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.epsilon = 1.0
        self.n_games = 0

    def get_action(self, state, position: Position):
        final_move = [0, 0, 0]
        if np.random.rand() < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        final_move[move] = 1
        return final_move

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * EPSILON_DECAY, MIN_EPSILON)

    def reset(self):
        self.n_games += 1
        self.decay_epsilon()

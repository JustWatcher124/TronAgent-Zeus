from collections import deque
from model import Linear_QNet, QTrainer
import random
import numpy as np
import torch
from settings import EPSILON_DECAY, GAMMA, MAX_MEMORY, BATCH_SIZE, LR, MIN_EPSILON


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 1 # randomness
        self.gamma = GAMMA # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(25, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    def epsilon_decay(self):
        if self.epsilon <= MIN_EPSILON:
            self.epsilon = MIN_EPSILON 
        else:
            self.epsilon *= EPSILON_DECAY
        print(self.epsilon)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon_decay()
        final_move = [0, 0, 0, 0]
        if np.random.random() < self.epsilon:
            move = np.random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

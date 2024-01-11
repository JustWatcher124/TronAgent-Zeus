from collections import deque
from settings import MAX_MEMORY, BATCH_SIZE
import random
import torch

class TronModel:
    def __init__(self, tron_agent_config):
        # TODO: model, trainer
        self.model = tron_agent_config.model
        self.trainer = tron_agent_config.trainer
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

    def train_short_memory(self, state, action, reward, next_state, isCollision):
        self.trainer.train_step(state, action, reward, next_state, isCollision)

    def remember(self, state, action, reward, next_state, isCollision):
        self.memory.append((state, action, reward, next_state, isCollision))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def get_next_move(self, epsilon, state):
        # Random moves : tradeoff exploration / exploitation
        final_move = [0, 0, 0]
        if random.randint(0, 200) < epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = int(torch.argmax(prediction).item())
            final_move[move] = 1
        return final_move

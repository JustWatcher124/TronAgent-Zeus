from tronmodel import TronModel
from direction import Direction 
from point import Point
from collections import deque
import random
from settings import BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, MAX_MEMORY, BATCH_SIZE
import numpy as np
import torch

class TronAgent:
    def __init__(self, tron_agent_config):
        self.color = tron_agent_config.color
        self.head_color = tron_agent_config.head_color
        self.size = tron_agent_config.block_size
        self.direction = Direction.UP
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

        self.start_x = tron_agent_config.start_x
        self.start_y = tron_agent_config.start_y
        self.name = tron_agent_config.name

        # TODO: model, trainer
        self.model = tron_agent_config.model
        self.trainer = tron_agent_config.trainer

        self.tron_model = TronModel(tron_agent_config)

    def reset(self):
        self.cut_off_reward = 0
        self.direction = Direction.UP    
        self.head = Point(self.start_x, self.start_y)
        self.snake = [
            self.head, 
        ]

    def set_opponent(self, opponent):
        self.opponent = opponent

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
            # hits opponent
            print("Is collision? at", self.head)
            if pt in self.opponent.snake:
                self.opponent.cut_off_reward = 10
                print(self.name,"collided with", self.opponent.name, "at", self.head)
                return True
        else:
            if pt in self.opponent.snake:
                return True

        # hits boundary
        if pt.x > SCREEN_WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > SCREEN_HEIGHT - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False

    def move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
        self.snake.insert(0, self.head)

    def update(self, eps):
        epsilon = eps
        if epsilon < 0:
            epsilon = 0.01

        old_state = self.get_state()
        final_move = self.tron_model.get_next_move(epsilon, old_state)
        self.move(final_move)
        reward = 0 + self.cut_off_reward
        isCollision = False

        if self.is_collision():
            reward = -10
            isCollision = True

        new_state = self.get_state()

        self.tron_model.train_short_memory(old_state, final_move, reward, new_state, isCollision)
        self.tron_model.remember(old_state, final_move, reward, new_state, isCollision)
        
        return isCollision
    
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

    def get_state(self):
        head = self.head
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_l)) or
            (dir_u and self.is_collision(point_u)) or
            (dir_d and self.is_collision(point_d)),

            # Danger right
            (dir_u and self.is_collision(point_r)) or
            (dir_d and self.is_collision(point_l)) or
            (dir_l and self.is_collision(point_u)) or
            (dir_r and self.is_collision(point_d)),

            # Danger left
            (dir_d and self.is_collision(point_r)) or
            (dir_u and self.is_collision(point_l)) or
            (dir_r and self.is_collision(point_u)) or
            (dir_l and self.is_collision(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,
        ]
        
        return np.array(state, dtype=int)

    def get_action(self, epsilon, state):
        # Random moves : tradeoff exploration / exploitation
        self.epsilon = epsilon
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = int(torch.argmax(prediction).item())
            final_move[move] = 1
        return final_move

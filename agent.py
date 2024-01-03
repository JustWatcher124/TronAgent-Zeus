import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point, BLOCKSIZE

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

        # TODO: model, trainer
        self.trainer = None
        self.model = None

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - BLOCKSIZE, head.y)
        point_r = Point(head.x + BLOCKSIZE, head.y)
        point_u = Point(head.x, head.y - BLOCKSIZE)
        point_d = Point(head.x, head.y + BLOCKSIZE)

        dir_l = game.direction == direction.LEFT
        dir_r = game.direction == direction.RIGHT
        dir_u = game.direction == direction.UP
        dir_d = game.direction == direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collection(point_r)) or
            (dir_l and game.is_collection(point_l)) or
            (dir_u and game.is_collection(point_u)) or
            (dir_d and game.is_collection(point_d)),

            # Danger right
            (dir_u and game.is_collection(point_r)) or
            (dir_d and game.is_collection(point_l)) or
            (dir_l and game.is_collection(point_u)) or
            (dir_r and game.is_collection(point_d)),

            # Danger left
            (dir_d and game.is_collection(point_r)) or
            (dir_u and game.is_collection(point_l)) or
            (dir_r and game.is_collection(point_u)) or
            (dir_l and game.is_collection(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            game.food.x < game.head.x, # food left
            game.food.x > game.head.x, # food right
            game.food.y < game.head.y, # food up
            game.food.y > game.head.y # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append(state, action, reward, next_state, done)

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)
        # get move
        final_move = agent.get_action(state_old)

        # perform moce and get state
        reward, done, score = game.play_stop(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                # TODO: agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record', record)
            # TDOO: plot

if __name__ == "__main__":
    train()

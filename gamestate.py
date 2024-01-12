from settings import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from point import Point
import numpy as np
class GameState:
    def __init__(self, agents):
        self.agents = agents # this is a list
        self.rows_len = SCREEN_HEIGHT / BLOCK_SIZE
        self.cols_len = SCREEN_WIDTH / BLOCK_SIZE
        self.state = self.get_initial_state()
    
    def get_game_state(self):
        rows_len = self.rows_len
        cols_len = self.cols_len
        for row in range(int(rows_len)):
            for col in range(int(cols_len)):
                curr_col = col * BLOCK_SIZE
                curr_row = row * BLOCK_SIZE
                current_point = Point(curr_col, curr_row)
                for index, agent in enumerate(self.agents):
                    if current_point in agent.snake: 
                        # plus one because 0 represents empty
                        self.state[row][col] = index + 1
        return np.array(self.state, dtype=int).flatten()

    def get_initial_state(self):
        rows_len = self.rows_len
        cols_len = self.cols_len
        
        state = []

        if rows_len % 1 != 0:
            print("Error")

        if cols_len % 1 != 0:
            print("Error")
        for row in range(int(rows_len)):
            state.append([])
            for col in range(int(cols_len)):
                state[row].append(0)

        return state

    def reset(self):
        self.state = self.get_initial_state()


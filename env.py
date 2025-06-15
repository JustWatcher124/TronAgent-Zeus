from typing import List, Tuple
import pygame
from torch import Block, positive
from collisions import Collisions
from direction import Direction
from position import Position
import numpy as np
import math
import random

from settings import AGENT_HEAD_COLOR, BACKGROUND_COLOR, BLOCK_SIZE, FPS, PLAYER_HEAD_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT, PLAYER_COLOR, AGENT_COLOR

pygame.init()
font = pygame.font.Font(size=25)


class ENV:
    def __init__(self) -> None:
        self._display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._player_reward = 0
        self._game_over = False
        self.n_games = 1

        # set window title
        pygame.display.set_caption("TRON")

        self._clock = pygame.time.Clock()
        self.reset()

    def reset(self):  # starts the environment
        directions = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        player_positions = [0.25, 0.5, 0.75]
        self.n_games += 1
        
        self._player_direction = random.choice(directions)
        ## CPU player
        self._player_head = Position(
            get_starting_pos_x(random.choice(player_positions)), 
            get_starting_pos_y(random.choice(player_positions)), 
        )
        self._player_tail = [
            self._player_head,
        ]
        self._player_score = 0
        
        ## AGENT player
        agent_positions = [0.2, 0.4, 0.6, 0.8, 0.9]
        self._agent_head = Position(
            get_starting_pos_x(random.choice(agent_positions)),
            get_starting_pos_y(random.choice(agent_positions))
        )
        self._agent_tail = [
            self._agent_head,
        ]
        self._agent_score = 0

        self._agent_reward = 0
        self._game_over = False
        self._frame_iteration = 0

    def play_step(self, agent_action: List[int]):
        self._frame_iteration += 1

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # make action
        self._player_move(self._get_player_action())
        self._agent_move(agent_action)
        collided = self._is_collision()

        if collided.player:
            self._game_over = True
            self._update_ui()
            self._clock.tick(FPS)
            return self._agent_reward, self._game_over, self._frame_iteration 

        if collided.agent:
            self._agent_reward = -10
            self._game_over = True
            self._update_ui()
            self._clock.tick(FPS)
            return self._agent_reward, self._game_over, self._frame_iteration 

        self._update_ui()
        self._clock.tick(FPS)
        self._agent_reward = 0

        return self._agent_reward, self._game_over, self._frame_iteration

    # unused
    # def _pick_random_turn(self):
    #     rand = np.random.randint(0,2)
    #     if rand:
    #         return [0, 1, 0]
    #     else:
    #         return [0, 0, 1]
    # ---
    def _get_player_action(self) -> List[int]:
        state = self._get_player_state()
        # if random > 0.01:
        if state[0] == 0:
            return [1, 0, 0]
        else:
            if np.random.random() > .5:
                if state[1] == 0:
                    return [0, 1, 0]
                else:
                    return [0, 0, 1]
            else:
                if state[2] == 0:
                    return [0, 0, 1]
                else:
                    return [0, 1, 0]
    
    def get_agent_state(self):  # gets the 25 long input data (5x5 centered around agent head) for ML input - pygame version
        radius = 2

        starting_x = BLOCK_SIZE * -radius + self._agent_head.x 
        starting_y = BLOCK_SIZE * -radius + self._agent_head.y

        ending_x = BLOCK_SIZE * radius + 1 + self._agent_head.x 
        ending_y = BLOCK_SIZE * radius + 1 + self._agent_head.y
        # print((starting_x, starting_y), (ending_x, ending_y))

        state = []

        for i in range(starting_y, ending_y, BLOCK_SIZE):
            for j in range(starting_x, ending_x, BLOCK_SIZE):
                position = Position(j, i)
                state.append(self._agent_pt_will_collide(position))
        

        return np.array(state, dtype=int)
    
    def _player_move(self, action: List):
        head, dir = self._move(action, self._player_direction, self._player_head)
        self._player_head = head
        self._player_direction = dir
        self._player_tail.insert(0,self._player_head)

    def _move(self, action, dir, head):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(dir)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        dir = new_dir

        x = head.x
        y = head.y
        if dir == Direction.RIGHT:
            x += BLOCK_SIZE
        elif dir == Direction.LEFT:
            x -= BLOCK_SIZE
        elif dir == Direction.DOWN:
            y += BLOCK_SIZE
        elif dir == Direction.UP:
            y -= BLOCK_SIZE

        head = Position(x, y)
        return head, dir 
        

    def _agent_move(self, action: List):
        x = self._agent_head.x
        y = self._agent_head.y

        if np.array_equal(action, [1, 0, 0, 0]):
            x -= BLOCK_SIZE
        elif np.array_equal(action, [0, 1, 0, 0]):
            x += BLOCK_SIZE
        elif np.array_equal(action, [0, 0, 1, 0]):
            y -= BLOCK_SIZE
        elif np.array_equal(action, [0, 0, 0, 1]):
            y += BLOCK_SIZE

        self._agent_head = Position(x, y)
        self._agent_tail.insert(0, self._agent_head)

    def _get_player_state(self):

        point_l = Position(self._player_head.x - BLOCK_SIZE, self._player_head.y)
        point_r = Position(self._player_head.x + BLOCK_SIZE, self._player_head.y)
        point_u = Position(self._player_head.x, self._player_head.y - BLOCK_SIZE)
        point_d = Position(self._player_head.x, self._player_head.y + BLOCK_SIZE)

        dir_l = self._player_direction == Direction.LEFT
        dir_r = self._player_direction == Direction.RIGHT
        dir_u = self._player_direction == Direction.UP
        dir_d = self._player_direction == Direction.DOWN

        state = [
             # Danger straight
            (dir_r and self._pt_will_collide(point_r)) or 
            (dir_l and self._pt_will_collide(point_l)) or 
            (dir_u and self._pt_will_collide(point_u)) or 
            (dir_d and self._pt_will_collide(point_d)),
#
            # Danger right
            (dir_u and self._pt_will_collide(point_r)) or 
            (dir_d and self._pt_will_collide(point_l)) or 
            (dir_l and self._pt_will_collide(point_u)) or 
            (dir_r and self._pt_will_collide(point_d)),

            # Danger left
            (dir_d and self._pt_will_collide(point_r)) or 
            (dir_u and self._pt_will_collide(point_l)) or 
            (dir_r and self._pt_will_collide(point_u)) or 
            (dir_l and self._pt_will_collide(point_d)),
        ]
        return np.array(state, dtype=int)

    def _is_collision(self) -> Collisions:
        player_collided = False
        agent_collided = False

        # player hits boundary
        if self._player_head.x > SCREEN_WIDTH - BLOCK_SIZE or self._player_head.x < 0 or self._player_head.y > SCREEN_HEIGHT - BLOCK_SIZE or self._player_head.y < 0:
            player_collided = True 

        # player hits self
        if self._player_head in self._player_tail[1:]:
            player_collided = True 

        # player hits agent
        if self._player_head in self._agent_tail:
            player_collided = True 

        # agent hits boundary
        if self._agent_head.x > SCREEN_WIDTH - BLOCK_SIZE or self._agent_head.x < 0 or self._agent_head.y > SCREEN_HEIGHT - BLOCK_SIZE or self._agent_head.y < 0:
            agent_collided = True 

        # agent hits self
        if self._agent_head in self._agent_tail[1:]:
            agent_collided = True 

        # agent hits player
        if self._agent_head in self._player_tail:
            agent_collided = True 

        return Collisions(player_collided, agent_collided)
    def _agent_pt_will_collide(self, pt):

        # player
        if pt.x > SCREEN_WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > SCREEN_HEIGHT - BLOCK_SIZE or pt.y < 0:
            return True
        
        # pt hits player
        if pt in self._player_tail:
            return True 

        # pt hits agent but not head
        if pt in self._agent_tail[1:]:
            return True 
        
        return False

    def _pt_will_collide(self, pt) -> bool:

        # player
        if pt.x > SCREEN_WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > SCREEN_HEIGHT - BLOCK_SIZE or pt.y < 0:
            return True
        
        # pt hits player
        if pt in self._player_tail:
            return True 

        # pt hits agent
        if pt in self._agent_tail:
            return True 
        
        return False

    def _update_ui(self):
        self._display.fill(BACKGROUND_COLOR)

        for pt in self._player_tail[1:]:
            pygame.draw.rect(self._display, PLAYER_COLOR, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        for pt in self._player_tail[:1]:
            pygame.draw.rect(self._display, PLAYER_HEAD_COLOR, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        for pt in self._agent_tail[1:]:
            pygame.draw.rect(self._display, AGENT_COLOR, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        for pt in self._agent_tail[:1]:
            pygame.draw.rect(self._display, AGENT_HEAD_COLOR, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Number of Games: " + str(self.n_games), True, TEXT)
        self._display.blit(text, [0, 0])
        pygame.display.flip()

#######################################################################

def get_starting_pos_y(num):
    if num > 1 or num < 0:
        print("Starting position y needs to be a decimal greater than 0 and less than 1")
        return 0
    return math.floor((SCREEN_HEIGHT / BLOCK_SIZE) * num) * BLOCK_SIZE

def get_starting_pos_x(num):
    if num > 1 or num < 0:
        print("Starting position x needs to be a decimal greater than 0 and less than 1")
        return 0
    return math.floor((SCREEN_WIDTH / BLOCK_SIZE) * num) * BLOCK_SIZE

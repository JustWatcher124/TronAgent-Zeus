from typing import List
import pygame
from collisions import Collisions
from direction import Direction
from position import Position
import numpy as np
import math

from settings import BACKGROUND_COLOR, BLOCK_SIZE, FPS, PLAYER_HEAD_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT

pygame.init()
font = pygame.font.Font(size=25)


class ENV:
    def __init__(self) -> None:
        self._screen_width = SCREEN_WIDTH        
        self._screen_height = SCREEN_HEIGHT        
        self._display = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._player_reward = 0
        self._game_over = False

        # set window title
        pygame.display.set_caption("TRON")

        self._clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        
        self._player_direction = Direction.RIGHT
        ## CPU player
        self._player_head = Position(
            get_starting_pos_x(0.5), 
            get_starting_pos_y(0.5), 
        )
        self._player_tail = [
            self._player_head,
        ]
        self._player_score = 0
        
        ## AGENT player
        # self.agent_head = Position(self.screen_width / 2, self.screen_height / 2)
        # self.agetn_tail = [
        #     self.agent_head,
        # ]
        # self.agent_score = 0

        self._player_reward = 0
        self._game_over = False
        self._frame_iteration = 0

    def play_step(self, player_action: List, agent_action: List):
        self._frame_iteration += 1

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # make action
        self._player_move(player_action)
        collided = self._is_collision()
        if collided.player or self._frame_iteration > 100 * len(self._player_tail):
            self._game_over = True
            self._player_reward = -10
            return self._player_reward, self._game_over, self._player_score

        self._update_ui()
        self._clock.tick(FPS)

        return self._player_reward, self._game_over, self._player_score
    
    def _player_move(self, action: List):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self._player_direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self._player_direction = new_dir

        x = self._player_head.x
        y = self._player_head.y
        if self._player_direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self._player_direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self._player_direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self._player_direction == Direction.UP:
            y -= BLOCK_SIZE

        self._player_head = Position(x, y)
        self._player_tail.insert(0,self._player_head)

    def _agent_move(self, action: List):
        pass

    def get_player_state(self):
        point_l = Position(head.x - 20, head.y)
        point_r = Position(head.x + 20, head.y)
        point_u = Position(head.x, head.y - 20)
        point_d = Position(head.x, head.y + 20)
        dir_l = self._player_direction == Direction.LEFT
        dir_r = self._player_direction == Direction.RIGHT
        dir_u = self._player_direction == Direction.UP
        dir_d = self._player_direction == Direction.DOWN
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
        ]
        return np.array(state, dtype=int)

    def _is_collision(self, pt: Position | None=None) -> Collisions:
        player_collided = False
        agent_collided = False

        if pt is None:
            # player hits boundary
            if self._player_head.x > self._screen_width - BLOCK_SIZE or self._player_head.x < 0 or self._player_head.y > self._screen_height - BLOCK_SIZE or self._player_head.y < 0:
                player_collided = True 

            # player hits self
            if self._player_head in self._player_tail[1:]:
                player_collided = True 

        else: 
            # pt hits boundary
            if pt.x > self._screen_width - BLOCK_SIZE or pt.x < 0 or pt.y > self._screen_height - BLOCK_SIZE or pt.y < 0:
                player_collided = True 

            # pt hits trail
            if pt in self._player_tail[1:]:
                player_collided = True 




        return Collisions(player_collided, agent_collided)

    def _update_ui(self):
        self._display.fill(BACKGROUND_COLOR)

        for pt in self._player_tail:
            pygame.draw.rect(self._display, PLAYER_HEAD_COLOR, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self._player_score), True, TEXT)
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

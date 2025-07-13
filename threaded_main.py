import time
import pygame
from env import BaseEnv
# from players import ScriptedPlayer, HumanPlayer, RLPlayer, ScriptedPlayerV2, Player
# from players import GAPlayer
# import pygame
from position import Position
from datetime import datetime
import os


USE_PYGAME_RENDERING = True
SCREEN_SIZE = 1024
FPS = 50
GRID_WIDTH = 50
GRID_HEIGHT = 50

COLOR_MAP = {
    0: (66, 66, 66),     # Empty
    1: (255, 64, 64),    # Player1 head
    2: (255, 20, 20),    # Player1 tail
    3: (64, 255, 64),    # Player2 head
    4: (20, 20, 255),    # Player2 tail
}

def threaded_main(p1, p2, episodes=200, render=False):
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT)
    if render:
        pygame.init()
        cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
        screen = pygame.display.set_mode((cell_size * env.width, cell_size * env.height))
        clock = pygame.time.Clock()

    for episode in range(episodes):
        
        env.reset()
        done = False
        while not done:
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            state_p1, head1, dir1 = env.get_player_view("p1")
            state_p2, head2, dir2 = env.get_player_view("p2")
            action1 = p1.get_action(state_p1, head1, dir1)
            action2 = p2.get_action(state_p2, head2, dir2)

            reward1, reward2, done, _ = env.play_step(action1, action2)

            next_state_p1, next_head1, _ = env.get_player_view("p1")
            next_state_p2, next_head2, _ = env.get_player_view("p2")

            p1.remember(state_p1, head1, next_head1, action1, reward1, next_state_p1, done)
            p2.remember(state_p2, head2, next_head2, action2, reward2, next_state_p2, done)

            if p1.can_train():
                p1.train()
                p1.reset()
                if (episode + 1) % 50 == 0 and (episode + 1) != 1:
                    p1.save_model(episode)
            if p2.can_train():
                p2.train()
                p2.reset()
                if (episode + 1) % 50 == 0 and (episode + 1) != 1:
                    p2.save_model(episode)

            if render:
                draw_grid(screen, env.grid, cell_size)
                pygame.display.flip()
                clock.tick(FPS)
    if p1.can_train():
        p1.save_model(episode)
    if p2.can_train():
        p2.save_model(episode)
    if render:
        pygame.quit()

def threaded_ga_main(p1, p2, generations=1000, render=False):
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT)
    episodes_per_generation = p1.games_per_generation

    if render:
        pygame.init()
        cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
        screen = pygame.display.set_mode((cell_size * env.width, cell_size * env.height))
        clock = pygame.time.Clock()

    for generation in range(generations):
        for episode in range(episodes_per_generation):
            env.reset()
            done = False

            while not done:
                if render:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return

                state_p1, head1, dir1 = env.get_player_view("p1")
                state_p2, head2, dir2 = env.get_player_view("p2")
                action1 = p1.get_action(state_p1, head1, dir1)
                action2 = p2.get_action(state_p2, head2, dir2)

                reward1, reward2, done, _ = env.play_step(action1, action2)
                p1.remember(reward1, done)

                if render:
                    draw_grid(screen, env.grid, cell_size)
                    pygame.display.flip()
                    clock.tick(FPS)

        if p1.can_evolve():
            p1.train()
            print(f'{p1.name} is evolving (generation {generation+1})')
            if (generation + 1) % 50 == 0 or generation == 1:
                p1.save_model(generation+1)
                # break # testing
        if p2.can_train():
            p2.train()
         # stop it
    if render:
        pygame.quit()
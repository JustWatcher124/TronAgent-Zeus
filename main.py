import time
import pygame
from env import BaseEnv, draw_grid
from players import ScriptedPlayer, HumanPlayer, RLPlayer, ScriptedPlayerV2, Player
from players import GAPlayer
# import pygame
from position import Position
from datetime import datetime
import os

USE_PYGAME_RENDERING = True
SCREEN_SIZE = 1024
FPS = 50
GRID_WIDTH = 50
GRID_HEIGHT = 50


def main(p1, p2, episodes=200, render=False, render_fps=50):
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT, fps=render_fps)
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
                clock.tick(env.fps)
    if p1.can_train():
        p1.save_model(episode)
    if p2.can_train():
        p2.save_model(episode)
    if render:
        pygame.quit()


def ga_main():
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT)
    p1 = GAPlayer(name="GA_P1", input_size=GRID_WIDTH*GRID_HEIGHT)
    p2 = ScriptedPlayerV2(name="Dummy_P2", direction='left')  #, input_size=GRID_WIDTH*GRID_HEIGHT)

    episodes_per_generation = p1.games_per_generation

    generations = 1000
    training_counter = 0
    
    
    for generation in range(generations):
        # print(f"\n=== Generation {generation} ===")
        for episode in range(episodes_per_generation):
            env.reset()
            step = 0
            done = False

            while not done:
                state_p1, head1, dir1 = env.get_player_view("p1")
                state_p2, head2, dir2 = env.get_player_view("p2")
                action1 = p1.get_action(state_p1, head1)
                action2 = p2.get_action(state_p2, head2, dir2)
                # r1, r2, done, winner = env.play_step(a1, a2)
                reward1, reward2, done, loser = env.play_step(action1, action2)
                # print(reward1, reward2)
                p1.remember(reward1, done)  # takes the next individual and trains it
                # p2.remember(reward2, done)
                step += 1

            # print(f"Episode {episode + 1}: Individual {p1.current_index} done")

        # Train GA after full population is evaluated
        
        if p1.can_evolve():
            p1.train()
            if (generation + 1) % 250 == 0:  # save every 250th generation
                p1.save_model(generation+1)
            # if training_counter % 50 == 0:

            #     print('Showing best Game')
            #     print(datetime.now())
                
            #     visualize_best_agent(env, p1.population[0], p2)
            # training_counter += 1
        if p2.can_train():
            p2.train()
        # generation += 1



def visualize_best_agent(env, best_individual, opponent):
    
    os.makedirs("screenshots", exist_ok=True)
    pygame.init()
    cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
    screen = pygame.display.set_mode((cell_size * env.width, cell_size * env.height))
    clock = pygame.time.Clock()
    done = False

    class VisualGAWrapper(Player):
        def __init__(self, individual):
            self.individual = individual
            self.name = "BestGA"

        def get_action(self, state, position: Position):
            move = self.individual.forward(state)
            action = [0, 0, 0]
            action[move % 3] = 1
            return action

    ga_player = VisualGAWrapper(best_individual)
    env.reset()
    frame_number = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        state_p1, head1, dir1 = env.get_player_view("p1")
        state_p2, head2, dir2 = env.get_player_view("p2")
        action1 = ga_player.get_action(state_p1, head1)
        action2 = opponent.get_action(state_p2, head2, dir2)

        _, _, done, loser = env.play_step(action1, action2)

        draw_grid(screen, env.grid, cell_size, frame_number)
        pygame.display.flip()
        clock.tick(FPS)
        frame_number += 1
    print(loser)
    time.sleep(1)
    pygame.quit()

if __name__ == "__main__":
    # main()  # works for every non-multiple game player (like GA)
    ga_main()  # trains the GAPlayer and shows best individual

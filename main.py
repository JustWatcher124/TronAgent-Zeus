import pygame
from agent import Agent
from env import ENV
from plot import plot
from settings import DEBUG
import numpy as np


def main() -> None:
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    env = ENV()
    env.reset()

    while True:  # there is no break condition - it would learn indefinitely - should fix
        # get old state
        state_old = env.get_agent_state()

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = env.play_step(final_move)
        state_new = env.get_agent_state()

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if DEBUG:
            while True:
                should_break = False
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            should_break = True
                        print('Model Vision Old')
                        print(np.array(state_old).reshape((5,5)))
                        print('Final Move')
                        print(final_move)
                        print('New State')
                        print(np.array(state_new).reshape((5,5)))
                        print(reward,done)
                if should_break:
                    break

        if done:
            agent.epsilon_decay()
            env.reset()
            agent.train_long_memory()

            if score > record:  # if current model is better than any model before
                record = score
                agent.model.save()  # save the current model

            print("game: ", env.n_games, "score: ", score, "record: ", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / env.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    main()

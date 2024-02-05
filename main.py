from agent import Agent
from env import ENV
from plot import plot


def main() -> None:
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    n_games = 0
    agent = Agent()
    env = ENV()
    env.reset()

    while True:
        # get old state
        state_old = env.get_agent_state()

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = env.play_step(final_move)
        state_new = env.get_agent_state()

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            env.reset()
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("game: ", n_games, "score: ", score, "record: ", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / n_games + 1
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

        n_games += 1

if __name__ == "__main__":
    main()

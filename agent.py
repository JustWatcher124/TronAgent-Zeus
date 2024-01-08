from agentresults import AgentResults
from game import SnakeGameAI
from helper import plot
from plot_results import ResultToPlot

def get_agents_results(agents, n_games):
    agents_results = []
    for agent in agents:
        isCollision, score = agent.update(80 - n_games)
        result = AgentResults(score, isCollision)
        agents_results.append(result)
    return agents_results


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGameAI()
    agents = game.agents
    n_games = 0
    while True:
        score = 0
        
        results = get_agents_results(agents, n_games)

        game.play_step()

        done = False

        for res in results:
            if res.isCollision:
                done = True
                break

        if done:
            # train long memory
            game.reset()
            n_games += 1

            for agent in agents:
                agent.train_long_memory()

            # if score > record:
            #     record = score
            #     tron_agent.model.save()
            #
            results_to_plot = []
            for res in results:
                plot_scores.append(res.score)
                total_score += res.score
                mean_score = total_score / n_games
                plot_mean_scores.append(mean_score)
                scores = ResultToPlot(plot_scores, plot_mean_scores)
                results_to_plot.append(scores)
            plot(results_to_plot)
            
            print('Game', n_games, 'Score', score, 'Record', record)

if __name__ == "__main__":
    train()

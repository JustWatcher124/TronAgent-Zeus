from agentresults import AgentResults
from game import SnakeGameAI
from helper import plot

def get_agents_results(agents, n_games):
    agents_results = []
    for agent in agents:
        isCollision, score = agent.update(80 - n_games)
        result = AgentResults(score, isCollision)
        agents_results.append(result)
        if isCollision:
            break
    return agents_results


def train():
    agent_one_wins = 0
    agent_two_wins = 0
    record = 0
    game = SnakeGameAI()
    agents = game.agents
    n_games = 0
    while True:
        score = 0
        loser = -1
        
        results = get_agents_results(agents, n_games)

        game.play_step()

        done = False

        for idx in range(len(results)):
            if results[idx].isCollision:
                done = True
                loser = idx
                score = results[idx].score
                break

        if loser == 0:
            agent_two_wins += 1

        if loser == 1:
            agent_one_wins += 1

        if done:
            # train long memory
            game.reset()
            n_games += 1

            for agent in agents:
                agent.train_long_memory()

            if score > record:
                record = score
                agents[loser].model.save()

            # plot_scores.append(results[0].score)
            # total_score += results[0].score
            # mean_score = total_score / n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)
            
            print('Game', n_games, 'Record', record, 'loser', loser, 'Agent_One_Wins', agent_one_wins, 'Agent_Two_Wins', agent_two_wins)

if __name__ == "__main__":
    train()

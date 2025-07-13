import itertools
from env import BaseEnv, draw_grid
from players import GAPlayer, RLPlayer, ScriptedPlayer, ScriptedPlayerV2
from model import Linear_QNet
import torch
import pickle
import os
import pygame
from env import BaseEnv, draw_grid, COLOR_MAP  # color map is needed for text display on the screenshots
from position import Position
import json
import pygame.freetype
from loading import load_rl_player, load_ga_player, get_builtin_bot
from main import SCREEN_SIZE, GRID_WIDTH, GRID_HEIGHT
EPISODES = 10  # how many games each two opponents get for figuring out who is better


def run_matchmaking(model_specs):
    players = []
    for spec in model_specs:
        if spec['type'] == 'rl':
            p = load_rl_player(spec['name'], spec['path'], spec['input_size'], spec['subgrid_size'])
        elif spec['type'] == 'ga':
            p = load_ga_player(spec['name'], spec['path'])
        elif spec['type'] == 'builtin':
            p = get_builtin_bot(spec['bot'], spec['name'])
        else:
            raise ValueError("Unsupported model type")
        players.append(p)

    results = {}
    scores = {p.name: 0 for p in players}

    for p1, p2 in itertools.combinations(players, 2):
        # s1, s2 = match(p1, p2)
        s1, s2 = MATCH_FUNCTION(p1, p2)
        scores[p1.name] += s1
        scores[p2.name] += s2
        results[(p1.name, p2.name)] = (s1, s2)

    print("\nMatch Results:")
    for (n1, n2), (s1, s2) in results.items():
        print(f"{n1} vs {n2} --> {s1}:{s2}")

    print("\nFinal Rankings (by total wins):")
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    for rank, (name, score) in enumerate(ranked, 1):
        print(f"{rank}. {name} - {score} pts")

def match(player1, player2, episodes=EPISODES):
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT)
    score1, score2 = 0, 0
    for _ in range(episodes):
        env.reset()
        done = False
        while not done:
            s1, h1, d1 = env.get_player_view("p1")
            s2, h2, d2 = env.get_player_view("p2")
            a1 = player1.get_action(s1, h1, d1)
            a2 = player2.get_action(s2, h2, d2)
            r1, r2, done, winner = env.play_step(a1, a2)
            if done:
                if winner == 'p1':
                    score1 += 1
                elif winner == 'p2':
                    score2 += 1
    return score1, score2


def visualize_match(player1, player2, episodes=10, base_path="matchmaking_screens"):
    env = BaseEnv(width=GRID_WIDTH, height=GRID_HEIGHT)
    os.makedirs(base_path, exist_ok=True)
    match_dir = os.path.join(base_path, f"{player1.name}-{player2.name}")
    os.makedirs(match_dir, exist_ok=True)

    pygame.init()
    pygame.freetype.init()
    font = pygame.freetype.SysFont("Arial", 16)
    cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
    screen = pygame.display.set_mode((cell_size * env.width, cell_size * env.height))

    score1, score2 = 0, 0

    for episode in range(episodes):
        env.reset()
        done = False
        frame_number = 0
        episode_dir = os.path.join(match_dir, f"episode_{episode}")
        os.makedirs(episode_dir, exist_ok=True)

        while not done:
            s1, h1, d1 = env.get_player_view("p1")
            s2, h2, d2 = env.get_player_view("p2")
            a1 = player1.get_action(s1, h1, d1)
            a2 = player2.get_action(s2, h2, d2)
            r1, r2, done, winner = env.play_step(a1, a2)

            if done:
                if winner == 'p1':
                    score1 += 1
                elif winner == 'p2':
                    score2 += 1

            draw_grid(screen, env.grid, cell_size)
            font.render_to(screen, (10, 10), f"P1: {player1.name}", COLOR_MAP[1])
            font.render_to(screen, (10, 30), f"P2: {player2.name}", COLOR_MAP[3])
            pygame.image.save(screen, os.path.join(episode_dir, f"frame_{frame_number:05d}.png"))
            frame_number += 1
         # Write JSON summary
        winner_name = None if winner == 'both' else player1.name if winner == 'p1' else player2.name
        loser_name = None if winner == 'both' else player2.name if winner == 'p1' else player1.name
        summary = {
            "match": f"{player1.name} vs {player2.name}",
            "episode": episode,
            "winner": winner_name,
            "loser": loser_name,
            "score": {
                player1.name: score1,
                player2.name: score2
            },
            "frames": frame_number
        }
        with open(os.path.join(episode_dir, "summary.json"), 'w') as f:
            json.dump(summary, f, indent=2)
    pygame.quit()
    return score1, score2



if __name__ == "__main__":
    # MATCH_FUNCTION = visualize_match
    MATCH_FUNCTION = match

    model_specs = [
        {"name": "GA_NPNET_5x5", "type": "ga", "path":      "modelsaves/GA_NPNET_5x5_input25_generation200.pkl", "input_size": 25, "subgrid_size": 5},
        {"name": "GA_NPNET_7x7", "type": "ga", "path":      "modelsaves/GA_NPNET_7x7_input49_generation200.pkl", "input_size": 49, "subgrid_size": 7},
        {"name": "GA_NPNET_9x9", "type": "ga", "path":      "modelsaves/GA_NPNET_9x9_input81_generation200.pkl", "input_size": 81, "subgrid_size": 9},
        {"name": "GA_NPNET_11x11", "type": "ga", "path":    "modelsaves/GA_NPNET_11x11_input121_generation200.pkl", "input_size": 121, "subgrid_size": 11},
        {"name": "GA_NPNET_Full", "type": "ga", "path":     "modelsaves/GA_NPNET_Full_input2500_generation200.pkl", "input_size": 2500, "subgrid_size": None},
        {"name": "GA_KERAS_5x5", "type": "ga", "path":      "modelsaves/GA_KERAS_5x5_input25_generation200.pkl", "input_size": 25, "subgrid_size": 5},
        {"name": "GA_KERAS_7x7", "type": "ga", "path":      "modelsaves/GA_KERAS_7x7_input49_generation200.pkl", "input_size": 49, "subgrid_size": 7},
        {"name": "GA_KERAS_9x9", "type": "ga", "path":      "modelsaves/GA_KERAS_9x9_input81_generation200.pkl", "input_size": 81, "subgrid_size": 9},
        {"name": "GA_KERAS_11x11", "type": "ga", "path":    "modelsaves/GA_KERAS_11x11_input121_generation200.pkl", "input_size": 121, "subgrid_size": 11},
        {"name": "GA_KERAS_Full", "type": "ga", "path":     "modelsaves/GA_KERAS_Full_input2500_generation200.pkl", "input_size": 2500, "subgrid_size": None},
        {"name": "RL_5x5", "type": "rl", "path":            "modelsaves/RL_5x5_input25_episode200.pth", "input_size": 25, "subgrid_size": 5},
        {"name": "RL_7x7", "type": "rl", "path":            "modelsaves/RL_7x7_input49_episode200.pth", "input_size": 49, "subgrid_size": 7},
        {"name": "RL_9x9", "type": "rl", "path":            "modelsaves/RL_9x9_input81_episode200.pth", "input_size": 81, "subgrid_size": 9},
        {"name": "RL_11x11", "type": "rl", "path":          "modelsaves/RL_11x11_input121_episode200.pth", "input_size": 121, "subgrid_size": 11},
        {"name": "RL_Full", "type": "rl", "path":           "modelsaves/RL_Full_input2500_episode200.pth", "input_size": 2500, "subgrid_size": None},
        {"name": "ForwardBot", "type": "builtin", "bot": "forward_bot"},
        {"name": "Dodger", "type": "builtin", "bot": "dodger_left"}
    ]
    run_matchmaking(model_specs)
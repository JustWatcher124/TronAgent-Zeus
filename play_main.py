import pygame
# import torch
from env import BaseEnv, draw_grid
from players import HumanPlayer
from loading import load_rl_player, load_ga_player, get_builtin_bot
from main import SCREEN_SIZE, GRID_WIDTH, GRID_HEIGHT, main

# the trained models were trained with BaseEnv random start=False and also always as Player1 (as P2 they freak out)
player2 = HumanPlayer(name="Human")

# Choose ONE of the following:

# GA example
# player1 = load_ga_player("GA_5x5", "modelsaves/GA_NPNET_7x7_input49_generation200.pkl")

# RL example
player1 = load_rl_player("RL_5x5", "modelsaves/RL_7x7_input49_episode200.pth", input_size=49, subgrid_size=7)
# see the modelsaves directory for the filenames
# Note for the arguments: subgrid = sqrt(input)

# Built-in bot example
# player1 = get_builtin_bot("forward_bot", "ForwardBot")
# player1 = get_builtin_bot("forward_bot", "ForwardBot")


main(player1, player2, episodes=1_000_000, render=True, render_fps=10)
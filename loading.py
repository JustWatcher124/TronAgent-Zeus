from players import GAPlayer, RLPlayer, ScriptedPlayer, ScriptedPlayerV2
from model import Linear_QNet
import pickle
import torch

def load_rl_player(name, path, input_size, subgrid_size):
    player = RLPlayer(name=name, input_size=input_size, subgrid_size=subgrid_size)
    model = Linear_QNet(input_size, 256, 3)
    model.load_state_dict(torch.load(path))
    player.model = model
    return player

def load_ga_player(name, path):
    with open(path, 'rb') as f:
        player = pickle.load(f)
    player.name = name
    return player

def get_builtin_bot(bot_type, name):
    if bot_type == "forward_bot":
        return ScriptedPlayer(name=name)
    elif bot_type == "dodger_left":
        return ScriptedPlayerV2(name=name, direction='left')
    elif bot_type == "dodger_right":
        return ScriptedPlayerV2(name=name, direction='right')
    else:
        raise ValueError(f"Unknown bot type: {bot_type}")
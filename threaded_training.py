import threading
from players import RLPlayer, ScriptedPlayerV2, GAPlayer
from threaded_main import threaded_main as main
from threaded_main import threaded_ga_main as ga_main
from main import GRID_WIDTH, GRID_HEIGHT

configs = [
    {"name": "RL_5x5", "input_size": 25, "subgrid_size": 5},
    {"name": "RL_7x7", "input_size": 49, "subgrid_size": 7},
    {"name": "RL_9x9", "input_size": 81, "subgrid_size": 9},
    {"name": "RL_11x11", "input_size": 121, "subgrid_size": 11},
    {"name": "RL_Full", "input_size": GRID_WIDTH*GRID_HEIGHT, "subgrid_size": None}
]

ga_configs = [
    {"name": "GA_KERAS_5x5", "input_size": 25, "subgrid_size": 5},
    {"name": "GA_KERAS_7x7", "input_size": 49, "subgrid_size": 7},
    {"name": "GA_KERAS_9x9", "input_size": 81, "subgrid_size": 9},
    {"name": "GA_KERAS_11x11", "input_size": 121, "subgrid_size": 11},
    {"name": "GA_KERAS_Full", "input_size": GRID_WIDTH * GRID_HEIGHT, "subgrid_size": None}
]

npnet_configs = [
    {"name": "GA_NPNET_5x5", "input_size": 25, "subgrid_size": 5},
    {"name": "GA_NPNET_7x7", "input_size": 49, "subgrid_size": 7},
    {"name": "GA_NPNET_9x9", "input_size": 81, "subgrid_size": 9},
    {"name": "GA_NPNET_11x11", "input_size": 121, "subgrid_size": 11},
    {"name": "GA_NPNET_Full", "input_size": GRID_WIDTH * GRID_HEIGHT, "subgrid_size": None}
]

def run_training_threaded(config):
    threads = []
    for cfg in configs:
        p1 = RLPlayer(name=cfg["name"], input_size=cfg["input_size"], subgrid_size=cfg["subgrid_size"])
        p2 = ScriptedPlayerV2(name="ScriptedP2")
        t = threading.Thread(target=main, args=(p1, p2), kwargs={"generations": 200, "render": False})
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def run_ga_training_threaded():
    threads = []
    for cfg in ga_configs:
        p1 = GAPlayer(name=cfg["name"], input_size=cfg["input_size"], subgrid_size=cfg["subgrid_size"])
        p2 = ScriptedPlayerV2(name="ScriptedP2")
        t = threading.Thread(target=ga_main, args=(p1, p2), kwargs={"generations": 200, "render": False})
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    run_ga_training_threaded()



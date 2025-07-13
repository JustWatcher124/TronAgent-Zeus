# Import all available player types
from .Script_and_Human import ScriptedPlayer, ScriptedPlayerV2, HumanPlayer
from .RLPlayer import RLPlayer
from .GAPlayer import GAPlayer
from .BasePlayer import Player

# To create your own player:
# 1. Inherit from the `Player` base class.
# 2. Implement the `get_action` method. Optionally override `remember`, `train`, `reset`, etc.
# 3. Place your class in a new or existing module.
# 4. Import it here and add it to the __all__ list to make it discoverable.

__all__ = ["ScriptedPlayer", "ScriptedPlayerV2", "HumanPlayer", "RLPlayer", "GAPlayer", "Player"]

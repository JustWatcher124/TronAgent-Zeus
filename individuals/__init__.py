from .keras import KerasIndividual
from .npnet import NPNetIndividual

# To add a new Individual type:
# 1. Create a class that implements a `.forward(state)` method and has a `.weights` attribute.
# 2. Optionally implement `.clone()` for reproduction and methods for serialization if needed.
# 3. Define the class in a new file or existing one.
# 4. Import it here and list it in __all__ to make it available to the GAPlayer.

__all__ = ["KerasIndividual", "NPNetIndividual"]
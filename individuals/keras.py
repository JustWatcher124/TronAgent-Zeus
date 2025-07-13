import tempfile
from tensorflow.keras.models import Sequential, clone_model, load_model
from tensorflow.keras.layers import Dense, Input
import pickle
import numpy as np


class KerasIndividual:
    """
    Represents a neural network-based individual using Keras for genetic algorithms.
    """

    def __init__(self, input_size, hidden_size, output_size, weights=None):
        """
        Initializes a fully connected feedforward network.

        Args:
            input_size (int): Number of input features.
            hidden_size (int): Number of hidden neurons.
            output_size (int): Number of output classes/actions.
            weights (np.ndarray, optional): Optional flat array of weights to load.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.model = Sequential([
            Input((input_size,)),
            Dense(hidden_size, activation='tanh'),
            Dense(output_size)
        ])
        if weights is not None:
            self.set_weights_flat(weights)
        self.fitness = 0.0

    @property
    def weights(self):
        """
        Returns flat representation of the model's weights.
        """
        return self.get_weights_flat()

    @weights.setter
    def weights(self, value):
        """
        Sets weights from a flat numpy array.
        """
        self.set_weights_flat(value)

    def forward(self, state):
        """
        Performs a forward pass and returns the index of the highest output.

        Args:
            state (array-like): Input vector.

        Returns:
            int: Index of the chosen action.
        """
        x = np.array(state).reshape(1, -1)
        output = self.model(x, training=False).numpy().flatten()
        return np.argmax(output)

    def get_weights_flat(self):
        """
        Flattens all weights and biases into a 1D array.

        Returns:
            np.ndarray: Flattened weights.
        """
        weights = self.model.get_weights()
        return np.concatenate([w.flatten() for w in weights])

    def set_weights_flat(self, flat_weights):
        """
        Reconstructs model weights from a flat array.

        Args:
            flat_weights (np.ndarray): Flattened weights.
        """
        shapes = [w.shape for w in self.model.get_weights()]
        new_weights = []
        idx = 0
        for shape in shapes:
            size = np.prod(shape)
            new_weights.append(flat_weights[idx:idx + size].reshape(shape))
            idx += size
        self.model.set_weights(new_weights)

    def clone(self):
        """
        Creates a deep copy of this individual with the same weights.

        Returns:
            KerasIndividual: Cloned instance.
        """
        clone = KerasIndividual(self.input_size, self.hidden_size, self.output_size)
        clone.set_weights_flat(self.get_weights_flat())
        return clone

    def __getstate__(self):
        """
        Custom serialization: converts Keras model to JSON and weight list.
        This avoids issues with pickling the model directly.

        Returns:
            dict: Serialized state.
        """
        state = self.__dict__.copy()
        state['model_json'] = self.model.to_json()
        state['model_weights'] = self.model.get_weights()
        del state['model']
        return state

    def __setstate__(self, state):
        """
        Custom deserialization: restores Keras model from JSON and weights.

        Args:
            state (dict): Serialized state from __getstate__.
        """
        from tensorflow.keras.models import model_from_json
        model = model_from_json(state['model_json'])
        model.set_weights(state['model_weights'])
        state.pop('model_json')
        state.pop('model_weights')
        self.__dict__.update(state)
        self.model = model

import numpy as np
from .BasePlayer import Player
from position import Position
import random
import os


class NPNetIndividual:
    """
    Lightweight neural network individual implemented with NumPy.
    Used in genetic algorithms without external ML libraries.
    """
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initializes architecture and random weights.

        Args:
            input_size (int): Number of input features.
            hidden_size (int): Number of hidden neurons.
            output_size (int): Number of output actions.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights = self._init_weights()
        self.fitness = 0.0

    def _init_weights(self):
        """
        Generates all weights and biases in a single flat vector.
        Layout:
            - W1: input -> hidden
            - b1: hidden bias
            - W2: hidden -> output
            - b2: output bias

        Returns:
            np.ndarray: Randomly initialized flat weights.
        """
        total_weights = (self.input_size + 1) * self.hidden_size + (self.hidden_size + 1) * self.output_size
        return np.random.randn(total_weights)

    def clone(self):
        """
        Creates a deep copy of this individual.

        Returns:
            NPNetIndividual: Cloned instance with copied weights.
        """
        clone = Individual(self.input_size, self.hidden_size, self.output_size)
        clone.weights = np.copy(self.weights)
        return clone

    def forward(self, state):
        """
        Performs a forward pass using the stored flat weights.

        Args:
            state (array-like): Input vector.

        Returns:
            int: Index of the selected action (highest activation).
        """
        idx = 0
        # decode W1
        W1 = self.weights[idx:idx + self.input_size * self.hidden_size].reshape(self.input_size, self.hidden_size)
        idx += self.input_size * self.hidden_size

        # decode b1
        b1 = self.weights[idx:idx + self.hidden_size]
        idx += self.hidden_size

        # decode W2
        W2 = self.weights[idx:idx + self.hidden_size * self.output_size].reshape(self.hidden_size, self.output_size)
        idx += self.hidden_size * self.output_size

        # decode b2
        b2 = self.weights[idx:idx + self.output_size]

        x = np.array(state).flatten()
        x = np.tanh(np.dot(x, W1) + b1)
        x = np.dot(x, W2) + b2
        return np.argmax(x)
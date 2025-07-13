import numpy as np
from .BasePlayer import Player
from position import Position
import random

import numpy as np
from .BasePlayer import Player
from position import Position
import random
import os

import tempfile


from tensorflow.keras.models import Sequential, clone_model, load_model
from tensorflow.keras.layers import Dense, Input
import pickle


class NPNetIndividual:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights = self._init_weights()
        self.fitness = 0.0

    def _init_weights(self):
        total_weights = (self.input_size + 1) * self.hidden_size + (self.hidden_size + 1) * self.output_size
        return np.random.randn(total_weights)

    def clone(self):
        clone = Individual(self.input_size, self.hidden_size, self.output_size)
        clone.weights = np.copy(self.weights)
        return clone

    def forward(self, state):
        idx = 0
        W1 = self.weights[idx:idx + self.input_size * self.hidden_size].reshape(self.input_size, self.hidden_size)
        idx += self.input_size * self.hidden_size
        b1 = self.weights[idx:idx + self.hidden_size]
        idx += self.hidden_size
        W2 = self.weights[idx:idx + self.hidden_size * self.output_size].reshape(self.hidden_size, self.output_size)
        idx += self.hidden_size * self.output_size
        b2 = self.weights[idx:idx + self.output_size]

        x = np.array(state).flatten()
        x = np.tanh(np.dot(x, W1) + b1)
        x = np.dot(x, W2) + b2
        return np.argmax(x)
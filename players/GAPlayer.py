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


class Individual:
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

class KerasIndividual:
    def __init__(self, input_size, hidden_size, output_size, weights=None):
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
        return self.get_weights_flat()

    @weights.setter
    def weights(self, value):
        self.set_weights_flat(value)

    def forward(self, state):
        x = np.array(state).reshape(1, -1)
        output = self.model(x, training=False).numpy().flatten()
        return np.argmax(output)

    def get_weights_flat(self):
        weights = self.model.get_weights()
        return np.concatenate([w.flatten() for w in weights])

    def set_weights_flat(self, flat_weights):
        shapes = [w.shape for w in self.model.get_weights()]
        new_weights = []
        idx = 0
        for shape in shapes:
            size = np.prod(shape)
            new_weights.append(flat_weights[idx:idx + size].reshape(shape))
            idx += size
        self.model.set_weights(new_weights)

    def clone(self):
        clone = KerasIndividual(self.input_size, self.hidden_size, self.output_size)
        clone.set_weights_flat(self.get_weights_flat())
        return clone

    # def __getstate__2(self):
    #     state = self.__dict__.copy()
    #     # Save model to bytes using temporary file
    #     with tempfile.NamedTemporaryFile(delete=False, suffix='.keras') as tmp:
    #         self.model.save(tmp.name)
    #         with open(tmp.name, 'rb') as f:
    #             state['model_bytes'] = f.read()
    #     state.pop('model')
    #     return state
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['model_json'] = self.model.to_json()
        state['model_weights'] = self.model.get_weights()
        del state['model']
        return state
    
    def __setstate__(self, state):
        from tensorflow.keras.models import model_from_json
        model = model_from_json(state['model_json'])
        model.set_weights(state['model_weights'])
        state.pop('model_json')
        state.pop('model_weights')
        self.__dict__.update(state)
        self.model = model

    # def __setstate__2(self, state):
    #     model_bytes = state.pop('model_bytes')
    #     with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as tmp:
    #         tmp.write(model_bytes)
    #         tmp.flush()
    #         from tensorflow.keras.models import load_model
    #         model = load_model(tmp.name)
    #     self.__dict__.update(state)
    #     self.model = model

class GAPlayer(Player):
    def __init__(self, name="GeneticAgent", input_size=25, subgrid_size=5, hidden_size=16, output_size=3, population_size=50):
        super().__init__(name)
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.population = [KerasIndividual(input_size, hidden_size, output_size) for _ in range(population_size)]
        self.current_index = 0
        self.total_games = 0
        self.games_per_generation = 100  # can be tuned
        self.subgrid_size = subgrid_size

    def _extract_state(self, grid, head: Position):
        if self.subgrid_size is None:
            return grid.flatten()
        if self.subgrid_size ** 2 != self.input_size:
            raise ValueError(f"Mismatch between subgrid_size={self.subgrid_size} and input_size={self.input_size}. subgrid_size needs to be the square root of input_size")
        half = self.subgrid_size // 2
        h, w = grid.shape
        cx, cy = head.x, head.y

        # Calculate bounds of the desired subgrid
        x_start = cx - half
        x_end = cx + half + 1
        y_start = cy - half
        y_end = cy + half + 1

        # Create empty grid with padding value (e.g., 5)
        padded_grid = np.full((self.subgrid_size, self.subgrid_size), fill_value=5, dtype=grid.dtype)

        # Compute actual indices to copy from original grid
        src_x_start = max(0, x_start)
        src_x_end = min(w, x_end)
        src_y_start = max(0, y_start)
        src_y_end = min(h, y_end)

        dst_x_start = src_x_start - x_start
        dst_x_end = dst_x_start + (src_x_end - src_x_start)
        dst_y_start = src_y_start - y_start
        dst_y_end = dst_y_start + (src_y_end - src_y_start)

        # Copy valid region into padded grid
        padded_grid[dst_y_start:dst_y_end, dst_x_start:dst_x_end] = grid[src_y_start:src_y_end, src_x_start:src_x_end]

        return padded_grid.flatten()

    def get_action(self, state, head: Position, _):
        state = self._extract_state(state, head)
        ind = self.population[self.current_index]
        move = ind.forward(state)
        action = [0, 0, 0]
        action[move % 3] = 1
        return action

    def remember(self, reward, done):
        self.population[self.current_index].fitness += reward
        if done:
            self.current_index = (self.current_index + 1) % self.population_size
            self.total_games += 1

    def evolve(self):
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)
        survivors = self.population[:self.population_size // 2]
        # print("Best Individual Fitness:", survivors[0].fitness)

        new_population = [ind.clone() for ind in survivors]
        while len(new_population) < self.population_size:
            p1, p2 = random.sample(survivors, 2)
            child = self._crossover(p1, p2)
            self._mutate(child)
            new_population.append(child)

        self.population = new_population
        self.current_index = 0
        for ind in self.population:
            ind.fitness = 0.0

    def _crossover(self, p1, p2):
        alpha = np.random.rand(len(p1.weights))
        child = p1.clone()
        child.weights = alpha * p1.weights + (1 - alpha) * p2.weights
        return child

    def _mutate(self, individual, mutation_rate=0.05):
        mask = np.random.rand(*individual.weights.shape) < mutation_rate
        individual.weights += np.random.randn(*individual.weights.shape) * mask

    def train(self):
        if self.can_evolve():
            self.evolve()
            self.total_games = 0

    def reset(self):
        pass

    def can_train(self):
        return True

    def can_evolve(self):
        return self.total_games >= self.games_per_generation
    
    def save_model(self, generation, file_name=None):
        model_folder_path = 'modelsaves'
        if file_name is None:
            file_name = f"{self.name}_input{self.input_size}_generation{generation}.pkl"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(file_name):
        # model_folder_path = ''
        # file_name = os.path.join(model_folder_path, file_name)
        with open(file_name, 'rb') as f:
            return pickle.load(f)


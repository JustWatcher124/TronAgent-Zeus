import numpy as np


class GAPlayer(Player):
    def __init__(self, name="GeneticAgent", input_size=25, hidden_size=16, output_size=3, population_size=50):
        super().__init__(name)
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.population = [self._init_weights() for _ in range(population_size)]
        self.scores = [0] * population_size
        self.current_index = 0

    def _init_weights(self):
        return np.random.randn((self.input_size + 1) * self.hidden_size + (self.hidden_size + 1) * self.output_size)

    def _forward(self, state, weights):
        idx = 0
        W1 = weights[idx:idx + self.input_size * self.hidden_size].reshape(self.input_size, self.hidden_size)
        idx += self.input_size * self.hidden_size
        b1 = weights[idx:idx + self.hidden_size]
        idx += self.hidden_size
        W2 = weights[idx:idx + self.hidden_size * self.output_size].reshape(self.hidden_size, self.output_size)
        idx += self.hidden_size * self.output_size
        b2 = weights[idx:idx + self.output_size]

        x = np.array(state).flatten()
        x = np.tanh(np.dot(x, W1) + b1)
        x = np.dot(x, W2) + b2
        return np.argmax(x)

    def get_action(self, state):
        weights = self.population[self.current_index]
        move = self._forward(state[0], weights)
        action = [0, 0, 0]
        action[move % 3] = 1
        return action

    def remember(self, _, __, reward, ___, done):
        self.scores[self.current_index] += reward
        if done:
            self.current_index += 1

    def evolve(self):
        # Selection
        sorted_indices = np.argsort(self.scores)[::-1]
        survivors = [self.population[i] for i in sorted_indices[:self.population_size // 2]]

        # Crossover + Mutation
        new_pop = survivors.copy()
        while len(new_pop) < self.population_size:
            p1, p2 = random.sample(survivors, 2)
            child = self._crossover(p1, p2)
            child = self._mutate(child)
            new_pop.append(child)

        self.population = new_pop
        self.scores = [0] * self.population_size
        self.current_index = 0

    def _crossover(self, p1, p2):
        alpha = np.random.rand(len(p1))
        return alpha * p1 + (1 - alpha) * p2

    def _mutate(self, child, mutation_rate=0.05):
        mutation = np.random.randn(*child.shape) * (np.random.rand(*child.shape) < mutation_rate)
        return child + mutation

    def train(self):
        self.evolve()

    def reset(self):
        pass  # could reset index etc. if needed
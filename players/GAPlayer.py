from individuals import *
from .BasePlayer import Player
from position import Position
from direction import Direction

class GAPlayer(Player):
    """
    Genetic Algorithm-based player that evolves a population of neural network agents.
    """
    def __init__(self, name="GeneticAgent", input_size=25, subgrid_size=5, hidden_size=16, output_size=3, population_size=50):
        super().__init__(name)
        self.population_size = population_size
        
        # change this line to any of the individuals in the __init__.py all list - you maybe need to change the values given to the init of that class
        self.population = [KerasIndividual(input_size, hidden_size, output_size) for _ in range(population_size)]
        
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.current_index = 0
        self.total_games = 0
        self.games_per_generation = 100  # can be tuned
        self.subgrid_size = subgrid_size

    def _extract_state(self, grid, head: Position):
        """
        Extracts a centered subgrid around the head. Pads if near edge.
        """
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
        """
        Returns an action from the current individual based on state.
        """
        state = self._extract_state(state, head)
        ind = self.population[self.current_index]
        move = ind.forward(state)
        action = [0, 0, 0]
        action[move % 3] = 1
        return action

    def remember(self, reward, done):
        """
        Updates fitness of current individual and rotates to next on episode end.
        """
        self.population[self.current_index].fitness += reward
        if done:
            self.current_index = (self.current_index + 1) % self.population_size
            self.total_games += 1

    def evolve(self):
        """
        Evolves the population using crossover and mutation on the fittest individuals.
        """
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)
        survivors = self.population[:self.population_size // 2]
        
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
        """
        Creates a new individual by blending weights from two parents.
        """
        alpha = np.random.rand(len(p1.weights))
        child = p1.clone()
        child.weights = alpha * p1.weights + (1 - alpha) * p2.weights
        return child

    def _mutate(self, individual, mutation_rate=0.05):
        """
        Applies random Gaussian mutation to individual weights.
        """
        mask = np.random.rand(*individual.weights.shape) < mutation_rate
        individual.weights += np.random.randn(*individual.weights.shape) * mask

    def train(self):
        """
        Evolves the population if enough games were played.
        """
        if self.can_evolve():
            self.evolve()
            self.total_games = 0

    def can_train(self):
        return True

    def can_evolve(self):
        return self.total_games >= self.games_per_generation
    
    def save_model(self, generation, file_name=None):
        """
        Saves the full GAPlayer object using pickle.
        """
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
        """
        Loads a GAPlayer object from file.
        """
        with open(file_name, 'rb') as f:
            return pickle.load(f)


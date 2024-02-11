# Tron Agents

This program simulates a game of Tron where one player is controlled by a machine learning (ML) agent and the other 
by a procedural computer player, utilizing PyTorch and Deep QNet learning.

### Methods

The program employs QNet learning, a form of reinforcement learning. The environment provides a 5x5 vision grid 
centered around the ML agent's position, enabling the model to anticipate potential threats.

The CPU player is programmed to move forward unless doing so would lead to a collision. In cases where moving straight 
is not possible, the CPU randomly decides to turn either left or right.

#### Hyper parameters

gamma: 0.999
learning rate: 0.001 using the Adam optimizer
minimum epsilon 0.001
epsilon decay rate per game: 0.995

#### Neural network architecture

The neural network has 25 input nodes, one hidden layer with 256 nodes and an output layer with 4 nodes corresponding
to 4 directions (left, right, up, down).

#### Training

The model has a max replay memory buffer of 100 000 and it trains in batch sizes of 1000.

### Highlights

After approximately 900 games or when the epsilon is sufficiently low for the model to be exploitive the vast majority of the time, 
the ML agent begins to surpass the CPU player, primarily due to the simplistic strategy employed by the CPU player.

### In conclusion

I had a hard time choosing the right information for the "environment" to expose to the model. I originally
was only passing in 3 values in an array like this: [danger straight, safe left, safe right] in reality this is something like
[1, 0, 0]. This was fine, but the model would walk right into a corner or trap itself somehow. So after doing some research I got the idea of
vision grids from a paper out of a university in Amsterdam. This significantly improved the model's ability to not get trapped, and improved the overall survival time.

### Game customization

To adjust various parameters of the game, open the settings.py file. Here, you'll find modifiable constants such as
GAMMA, the learning rate (LR), and options for color customization.

### Running the game

Have [Conda](https://www.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [Python](https://www.python.org/downloads/) installed on your machine

Clone this repo and enter to the cloned repo. Then run these commands in the terminal:
```bash
conda env create -f environment.yml

conda activate pygame_env
```

To run the game:
```bash
python main.py
```

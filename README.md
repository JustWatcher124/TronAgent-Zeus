# Tron Agents

This program simulates a game of Tron where one player is controlled by a machine learning (ML) agent and the other 
by a procedural computer player, utilizing PyTorch and Deep QNet learning.

### Methodology

The program employs QNet learning, a form of reinforcement learning. The environment provides a 3x3 vision grid 
centered around the ML agent's position, enabling the model to limitedly anticipate potential threats.

The CPU player is programmed to move forward unless doing so would lead to a collision. In cases where moving straight 
is not possible, the CPU randomly decides to turn either left or right.

### Highlights

After approximately 300 games, the ML agent begins to surpass the CPU player, primarily due to the simplistic 
strategy employed by the CPU player.

### In conclusion

Neural networks pose significant challenges in terms of debugging and interpretation. To enhance the model's
performance, I'd like to implement a 5x5 vision grid, allowing for more advanced planning. Additionally, 
introducing a more sophisticated CPU player could further test the ML agent's capabilities.

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

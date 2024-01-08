from collections import namedtuple
import math
from settings import BLOCK_SIZE, BLUE, ORANGE, SCREEN_HEIGHT, SCREEN_WIDTH
from model import Linear_QNet
from trainer import QTrainer

Agent = namedtuple('Agent','color, block_size, model, trainer, start_y, start_x')

# Use a decimal
def get_starting_pos_y(num):
    if num > 1 or num < 0:
        print("Starting position y needs to be a decimal greater than 0 and less than 1")
        return 0
    return math.floor((SCREEN_HEIGHT / BLOCK_SIZE) * num) * BLOCK_SIZE
def get_starting_pos_x(num):
    if num > 1 or num < 0:
        print("Starting position x needs to be a decimal greater than 0 and less than 1")
        return 0
    return math.floor((SCREEN_WIDTH / BLOCK_SIZE) * num) * BLOCK_SIZE
# AGENT1
AGENT_ONE_LR = 0.001
AGENT_ONE_GAMMA = 0.9 # not greater than 1
AGENT_ONE_HIDDEN_SIZE = 256 # hidden layer
AGENT_ONE_OUTPUT_SIZE = 3
AGENT_ONE_INPUT_SIZE = 7
AGENT_ONE_SAVE_FOLDER = './agent_one'
AGENT_ONE_STARTING_Y = get_starting_pos_y(.80)
AGENT_ONE_STARTING_X = get_starting_pos_x(0.75)

AGENT_ONE_MODEL = Linear_QNet(
    AGENT_ONE_INPUT_SIZE,
    AGENT_ONE_HIDDEN_SIZE,
    AGENT_ONE_OUTPUT_SIZE,
    AGENT_ONE_SAVE_FOLDER
)

AGENT_ONE_TRAINER = QTrainer(
    AGENT_ONE_MODEL,
    AGENT_ONE_LR,
    AGENT_ONE_GAMMA,
)

AGENT_ONE = Agent(
    ORANGE,
    BLOCK_SIZE,
    AGENT_ONE_MODEL,
    AGENT_ONE_TRAINER,
    AGENT_ONE_STARTING_Y,
    AGENT_ONE_STARTING_X
)

# AGENT2
AGENT_TWO_LR = 0.001
AGENT_TWO_GAMMA = 0.9 # not greater than 1
AGENT_TWO_HIDDEN_SIZE = 256 # hidden layer
AGENT_TWO_OUTPUT_SIZE = 3
AGENT_TWO_INPUT_SIZE = 7
AGENT_TWO_SAVE_FOLDER = './agent_two'
AGENT_TWO_STARTING_Y = get_starting_pos_y(.80)
AGENT_TWO_STARTING_X = get_starting_pos_x(0.25)

AGENT_TWO_MODEL = Linear_QNet(
    AGENT_TWO_INPUT_SIZE,
    AGENT_TWO_HIDDEN_SIZE,
    AGENT_TWO_OUTPUT_SIZE,
    AGENT_TWO_SAVE_FOLDER
)

AGENT_TWO_TRAINER = QTrainer(
    AGENT_TWO_MODEL,
    AGENT_TWO_LR,
    AGENT_TWO_GAMMA,
)

AGENT_TWO = Agent(
    BLUE,
    BLOCK_SIZE,
    AGENT_TWO_MODEL,
    AGENT_TWO_TRAINER,
    AGENT_TWO_STARTING_Y,
    AGENT_TWO_STARTING_X
)

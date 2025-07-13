import numpy as np
from position import Position
from direction import Direction
import pygame

COLOR_MAP = {
    0: (66, 66, 66),     # Empty
    1: (255, 64, 64),    # Player1 head
    2: (255, 20, 20),    # Player1 tail
    3: (64, 255, 64),    # Player2 head
    4: (20, 20, 255),    # Player2 tail
}

EMPTY = 0
P1_HEAD = 1
P1_TAIL = 2
P2_HEAD = 3
P2_TAIL = 4

DIRECTIONS = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

class BaseEnv:
    """
    A base environment class for a two-player grid-based game simulation, 
    inspired by the upstream ENV class. It handles movement, state tracking,
    and collision resolution for both players.
    """
    def __init__(self, width=25, height=25, random_spawn=False, fps=50):
        """
        Initialize the environment with a given grid size and spawn settings.

        Args:
            width (int): Width of the grid.
            height (int): Height of the grid.
            random_spawn (bool): Whether to spawn players at random positions.
            fps (int): Frames per second for rendering purposes.
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.random_spawn = random_spawn
        self.fps = fps
        self.reset()

    def reset(self):
        """
        Reset the environment to the initial state, optionally with random spawn.
        """
        self.grid.fill(EMPTY)
        self.frame = 0
        self.done = False

        if self.random_spawn:
            from random import randint
            def rand_pos():
                return Position(randint(0, self.width - 1), randint(0, self.height - 1))
            self.p1_head = rand_pos()
            self.p2_head = rand_pos()
            while self.p2_head == self.p1_head:
                self.p2_head = rand_pos()
        else:
            self.p1_head = Position(self.width // 4, self.height // 2)
            self.p2_head = Position(3 * self.width // 4, self.height // 2)

        self.p1_tail = [self.p1_head]
        self.p2_tail = [self.p2_head]

        self.p1_dir = Direction.RIGHT
        self.p2_dir = Direction.LEFT

        self.grid[self.p1_head.y, self.p1_head.x] = P1_HEAD
        self.grid[self.p2_head.y, self.p2_head.x] = P2_HEAD

    def play_step(self, action_p1, action_p2):
        """
        Advance the environment one frame by executing both players' actions.

        Args:
            action_p1 (list): One-hot action for player 1.
            action_p2 (list): One-hot action for player 2.

        Returns:
            Tuple[int, int, bool, str]: Rewards for p1 and p2, game status, and winner.
        """
        self.frame += 1
        self._move_player('p1', action_p1)
        self._move_player('p2', action_p2)

        dead_p1 = self._is_dead(self.p1_head, self.p1_tail, self.p2_tail)
        dead_p2 = self._is_dead(self.p2_head, self.p2_tail, self.p1_tail)

        self.done = dead_p1 or dead_p2

        if dead_p1 and not dead_p2:
            return -10, +10, self.done, 'p2'
        elif dead_p2 and not dead_p1:
            return +10, -10, self.done, 'p1'
        elif dead_p1 and dead_p2:
            return -10, -10, self.done, 'both'
        else:
            return 0, 0, self.done, None

    def _move_player(self, player, action):
        """
        Move the specified player based on the action taken.

        Args:
            player (str): 'p1' or 'p2'.
            action (list): One-hot action list.

        Returns:
            Tuple[int, bool]: Reward and death status.
        """
        head = getattr(self, f'{player}_head')
        direction = getattr(self, f'{player}_dir')
        tail = getattr(self, f'{player}_tail')

        new_head, new_dir = self._apply_action(action, direction, head)

        # Check for collision BEFORE touching the grid
        reward, dead = self._check_collision(new_head, tail, self.p2_tail if player == 'p1' else self.p1_tail)
        setattr(self, f'{player}_head', new_head)
        setattr(self, f'{player}_dir', new_dir)

        if not dead:
            tail.insert(0, new_head)
            head_val = P1_HEAD if player == 'p1' else P2_HEAD
            tail_val = P1_TAIL if player == 'p1' else P2_TAIL
            self.grid[new_head.y, new_head.x] = head_val
            if len(tail) > 1:
                self.grid[tail[1].y, tail[1].x] = tail_val

        return reward, dead

    def _apply_action(self, action, direction, head):
        """
        Compute the new head position and direction after applying an action.

        Args:
            action (list): One-hot encoded action.
            direction (Direction): Current direction.
            head (Position): Current head position.

        Returns:
            Tuple[Position, Direction]: New head position and direction.
        """
        idx = DIRECTIONS.index(direction)

        if action == [1, 0, 0]:
            new_dir = direction
        elif action == [0, 1, 0]:
            new_dir = DIRECTIONS[(idx + 1) % 4]
        elif action == [0, 0, 1]:
            new_dir = DIRECTIONS[(idx - 1) % 4]
        else:
            raise ValueError("Invalid action")

        x, y = head.x, head.y
        if new_dir == Direction.RIGHT:
            x += 1
        elif new_dir == Direction.LEFT:
            x -= 1
        elif new_dir == Direction.UP:
            y -= 1
        elif new_dir == Direction.DOWN:
            y += 1

        return Position(x, y), new_dir

    def _check_collision(self, head, own_tail, other_tail):
        """
        Check if a head position results in a collision.

        Returns:
            Tuple[int, bool]: Reward and collision flag.
        """
        if not (0 <= head.x < self.width and 0 <= head.y < self.height):
            return -10, True
        if head in own_tail[1:] or head in other_tail:
            return -10, True
        return 0, False

    def get_player_view(self, player='p1'):
        """
        Get the observable grid from a player's perspective.

        Returns:
            Tuple[np.ndarray, Position, Direction]
        """
        if player == 'p1':
            return self.grid.copy(), self.p1_head, self.p1_dir
        elif player == 'p2':
            return self._translate_grid(self.grid), self.p2_head, self.p2_dir
        else:
            raise ValueError("Unknown player")

    def _translate_grid(self, grid):
        """
        Flip the perspective of the grid for player 2 view.

        Returns:
            np.ndarray: Translated grid.
        """
        translated = grid.copy()
        translated[grid == P1_HEAD] = P2_HEAD + 10
        translated[grid == P1_TAIL] = P2_TAIL + 10
        translated[grid == P2_HEAD] = P1_HEAD
        translated[grid == P2_TAIL] = P1_TAIL
        translated[translated == P2_HEAD + 10] = P2_HEAD
        translated[translated == P2_TAIL + 10] = P2_TAIL
        return translated
    
    def _is_dead(self, head, own_tail, other_tail):
        """
        Check if a player is dead (collided with walls or any tails).

        Returns:
            bool
        """
        if not (0 <= head.x < self.width and 0 <= head.y < self.height):
            return True
        if head in own_tail[1:] or head in other_tail:
            return True
        return False

def draw_grid(screen, grid, cell_size, frame_number=None):
    """
    Render the game grid onto the Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        grid (np.ndarray): 2D array representing the game state.
        cell_size (int): Size of each grid cell in pixels.
        frame_number (int, optional): Frame number for potential future use (unused).
    """
    screen.fill((66, 66, 66))
    h, w = grid.shape
    for y in range(h):
        for x in range(w):
            value = grid[y, x]
            color = COLOR_MAP.get(value, (0, 0, 0))
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
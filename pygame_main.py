import pygame
import time
from env import BaseEnv
from players import ScriptedPlayer, HumanPlayer, ScriptedPlayerV2

SCREEN_SIZE = 1024
FPS = 10

COLOR_MAP = {
    0: (66, 66, 66),     # Empty
    1: (255, 64, 64),    # Player1 head
    2: (255, 20, 20),    # Player1 tail
    3: (64, 255, 64),    # Player2 head
    4: (20, 20, 255),    # Player2 tail
}

def draw_grid(screen, grid, cell_size):
    screen.fill((66, 66, 66))
    h, w = grid.shape
    for y in range(h):
        for x in range(w):
            value = grid[y, x]
            color = COLOR_MAP.get(value, (0, 0, 0))
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

def main():
    pygame.init()
    env = BaseEnv(width=50, height=50)  # Try changing these to test scaling
    cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
    window_width = cell_size * env.width
    window_height = cell_size * env.height

    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()

    p1 = HumanPlayer("P1")
    p2 = ScriptedPlayer("P2")

    episodes = 3
    for episode in range(episodes):
        env.reset()
        done = False
        print(f"\n--- Episode {episode + 1} ---")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            state1 = env.get_player_view("p1")
            state2 = env.get_player_view("p2")
            a1 = p1.get_action(state1)
            a2 = p2.get_action(state2)
            r1, r2, done = env.play_step(a1, a2)

            draw_grid(screen, env.grid, cell_size)
            pygame.display.flip()
            clock.tick(FPS)

        print(f"Episode {episode + 1} ended: Reward P1: {r1}, P2: {r2}")
        time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    main()
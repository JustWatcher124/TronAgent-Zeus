import time
import pygame
from env import BaseEnv
from players import ScriptedPlayer, HumanPlayer, RLPlayer, ScriptedPlayerV2

USE_PYGAME_RENDERING = False
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
    env = BaseEnv(width=50, height=50)
    # p1 = HumanPlayer(name="P1") if USE_PYGAME_RENDERING else ScriptedPlayer(name="P1")
    p1 = RLPlayer(name='P2')
    p2 = ScriptedPlayerV2(name="P2")
    episodes = 0

    if USE_PYGAME_RENDERING:
        pygame.init()
        cell_size = min(SCREEN_SIZE // env.width, SCREEN_SIZE // env.height)
        screen = pygame.display.set_mode((cell_size * env.width, cell_size * env.height))
        clock = pygame.time.Clock()
    episode = 0
    while episode <= episodes or episodes == 0:
    # for episode in range(episodes):
        env.reset()
        done = False
        print(f"\n--- Episode {episode + 1} ---")
        while not done:
            if USE_PYGAME_RENDERING:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            state1, head1 = env.get_player_view("p1")
            state2, head2 = env.get_player_view("p2")
            a1 = p1.get_action(state1, head1)
            a2 = p2.get_action(state2, head2)
            r1, r2, done = env.play_step(a1, a2)

            if USE_PYGAME_RENDERING:
                draw_grid(screen, env.grid, cell_size)
                pygame.display.flip()
                clock.tick(FPS)

        print(f"Episode {episode + 1} ended: Reward P1: {r1}, P2: {r2}")
        episode += 1
        if USE_PYGAME_RENDERING:
            time.sleep(1)

    if USE_PYGAME_RENDERING:
        pygame.quit()

if __name__ == "__main__":
    main()

import pygame
from tronagent import TronAgent
import math
from agentconfigs import AGENT_ONE, AGENT_TWO
from settings import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class SnakeGameAI:
    
    def __init__(self):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.agents = [TronAgent(AGENT_ONE), TronAgent(AGENT_TWO)]
        self.n_games = 0
        self.reset()
        
    def reset(self):
        
        for agent in self.agents:
            agent.reset()

        # this could be better lol
        self.agents[0].set_opponent(self.agents[1])
        self.agents[1].set_opponent(self.agents[0])

        self.score = 0
        self.frame_iteration = 0
        if self.n_games == 0:
            self.n_games = 0.1
        else:
            self.n_games += 1
        
    def play_step(self):

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for agent in self.agents:

            for pt in agent.snake:
                pygame.draw.rect(self.display, agent.color, pygame.Rect(pt.x, pt.y, agent.size, agent.size))
        
        text = font.render("Games: " + str(math.floor(self.n_games)), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

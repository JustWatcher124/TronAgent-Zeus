import pygame
from gamestate import GameState
from tronagent import TronAgent
import math
from agentconfigs import AGENT_ONE, AGENT_TWO
from settings import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, DEBUG

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

        self.epsilon_min = 0.05 # minimum exploration rate
        self.epsilon = 1 # initial exploration rate
        self.epsilon_decay = 0.995

        self.agent_one = TronAgent(AGENT_ONE)
        self.agent_one_wins = 0

        self.agent_two = TronAgent(AGENT_TWO)
        self.agent_two_wins = 0

        self.game_state_machine = GameState([self.agent_one, self.agent_two])

        self.n_games = 0
        self.winner = ""
        self.game_done = False
        self.reset()

    def get_epsilon(self):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)
        
    def reset(self):
        
        # this could be better lol
        self.game_done = False
        self.winner = ""

        self.game_state_machine.reset()

        self.agent_one.set_opponent(self.agent_two)
        self.agent_one.set_game_state_machine(self.game_state_machine)
        self.agent_one.reset()

        self.agent_two.set_opponent(self.agent_one)
        self.agent_two.set_game_state_machine(self.game_state_machine)
        self.agent_two.reset()


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

        self.get_epsilon()
        ## START HERE ##
        agent_one_isCollision = self.agent_one.update(self.epsilon)
        if agent_one_isCollision:
            self.winner = self.agent_two.name
            self.agent_two_wins += 1
            self.game_done = True

        agent_two_isCollision = self.agent_two.update(self.epsilon)
        if agent_two_isCollision:
            self.winner = self.agent_one.name
            self.agent_one_wins += 1
            self.game_done = True

            # This is for evenness
            agent_one_isCollision = self.agent_one.update(self.epsilon)
            if agent_one_isCollision:
                self.winner = self.agent_two.name
                self.agent_two_wins += 1
                self.game_done = True

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        if self.game_done:

            # train long memory
            self.agent_one.tron_model.train_long_memory()
            self.agent_two.tron_model.train_long_memory()

            self.reset()

        if DEBUG:
            print(self.agent_one.name, "collision:", agent_one_isCollision, "wins:", self.agent_one_wins)
            print(self.agent_two.name, "collision:", agent_two_isCollision, "wins:", self.agent_two_wins)
            while True:
                should_break = False
                text = font.render("Debug", True, WHITE)
                self.display.blit(text, [200, 200])
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            should_break = True
                if should_break:
                    break

        
    def _update_ui(self):
        self.display.fill(BLACK)
        agent = self.agent_one
        pygame.draw.rect(self.display, agent.head_color, pygame.Rect(agent.head.x, agent.head.y, agent.size, agent.size))
        for pt in agent.snake[1:]:
            pygame.draw.rect(self.display, agent.color, pygame.Rect(pt.x, pt.y, agent.size, agent.size))
        agent_two = self.agent_two
        pygame.draw.rect(self.display, agent_two.head_color, pygame.Rect(agent_two.head.x, agent_two.head.y, agent_two.size, agent_two.size))
        for pt in agent_two.snake[1:]:
            pygame.draw.rect(self.display, agent_two.color, pygame.Rect(pt.x, pt.y, agent_two.size, agent_two.size))
        
        text = font.render("Games: " + str(math.floor(self.n_games)), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

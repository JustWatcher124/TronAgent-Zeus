import pygame
from game_object.ObjectManager import GetObjects
from settings import BACKGROUND_COLOR, BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


class Screen:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR) 
        self.render_objects()
            
        pygame.display.flip()

    def render_objects(self) -> None:
        for object in GetObjects():
            pygame.draw.rect(
                self.screen, 
                object.color, 
                pygame.Rect(
                    object.position.x, 
                    object.position.y, 
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )

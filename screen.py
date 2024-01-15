import pygame
from game_object.ObjectManager import ObjectManager
from settings import BACKGROUND_COLOR, BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


class Screen:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

    def render(self, object_man: ObjectManager) -> None:
        self.screen.fill(BACKGROUND_COLOR) 
        self.render_objects(object_man)
            
        pygame.display.flip()

    def render_objects(self, object_man) -> None:
        for object in object_man.get_objects():
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

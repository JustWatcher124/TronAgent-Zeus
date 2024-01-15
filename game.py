import pygame
from pygame.time import Clock
from PygameEvents import PygameEvents
from lightcycle.LightCycleHead import LightCycleHead
from game_object.ObjectManager import ObjectManager
from position import Position
from settings import BLOCK_SIZE, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from screen import Screen

pygame.init()

class Game:
    _running: bool
    _clock: Clock
    _screen: Screen
    _object_manager: ObjectManager
    _pygame_events: PygameEvents

    def __init__(self) -> None:
        self._running = True
        self._clock = pygame.time.Clock()
        self._screen = Screen()
        self._object_manager = ObjectManager()
        self._pygame_events = PygameEvents()
        
    def start(self) -> None:
        self._load_objects()
        self._run()

    def _run(self) -> None:

        while self._running:
            self._pygame_events.update()
            for event in self._pygame_events.events:
                if event.type == pygame.QUIT:
                    print("hello")
                    pygame.quit()
            self._object_manager.update()
            self._screen.render(self._object_manager)
            self._clock.tick(FPS)

        pygame.quit()

    def _load_objects(self):
        player_one = LightCycleHead(Position(500, 500), "player_one", pygame.Color(255,255,255))
        self._object_manager.attach(player_one)

    def _load_walls(self):
        x_len = int(SCREEN_WIDTH / BLOCK_SIZE) - 1
        y_len = int(SCREEN_HEIGHT / BLOCK_SIZE) - 1

        # TOP
        for position in range(1, x_len, BLOCK_SIZE):
            print(position)

        

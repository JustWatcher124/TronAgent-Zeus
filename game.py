import pygame
from pygame.time import Clock
from ObjectLoader import ObjectLoader
from PygameEvents import PygameEvents
from game_object.CollisionManager import CheckForCollision, ResetCollisionManager
from game_object.ObjectManager import ResetObjectManager, UpdateObjects
from settings import FPS
from screen import Screen
from singleton.SingletonMeta import SingletonMeta

pygame.init()

class Game(metaclass=SingletonMeta):
    _running: bool
    _clock: Clock
    _screen: Screen
    _pygame_events: PygameEvents

    def __init__(self) -> None:
        self._running = True
        self._clock = pygame.time.Clock()
        self._screen = Screen()
        self._pygame_events = PygameEvents()
        self._object_loader = ObjectLoader()
        self._n_games = 0
        self._new_game = False
        
    def start(self) -> None:
        self._object_loader.load_objects()
        self._run()

    def reset(self) -> None:
        ResetObjectManager()
        ResetCollisionManager()
        self._object_loader.load_objects()
        self._n_games += 1

    def _run(self) -> None:

        while self._running:
            self._pygame_events.update()
            for event in self._pygame_events.events:
                if event.type == pygame.QUIT:
                    pygame.quit()

            if self._new_game:
                self.reset()

            UpdateObjects()
            self._screen.render()
            CheckForCollision()
            self._clock.tick(FPS)

        pygame.quit()

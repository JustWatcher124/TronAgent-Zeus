import pygame
from pygame.time import Clock
from ObjectLoader import ObjectLoader
from PygameEvents import PygameEvents
from game_object.CollisionManager import CollisionManger
from game_object.ObjectManager import ObjectManager
from settings import FPS
from screen import Screen
from singleton.SingletonMeta import SingletonMeta

pygame.init()

class Game(metaclass=SingletonMeta):
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
        self._object_loader = ObjectLoader()
        self._collision_manager = CollisionManger()
        self._n_games = 0
        self._new_game = False
        
    def start(self) -> None:
        self._object_loader.load_objects()
        self._run()

    def reset(self) -> None:
        self._object_manager.reset()
        self._collision_manager.reset()
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

            self._object_manager.update()
            self._collision_manager.check_for_collisions()
            self._screen.render(self._object_manager)
            self._clock.tick(FPS)

        pygame.quit()

from typing import List
from pygame.event import Event
import pygame
from singleton.SingletonMeta import SingletonMeta


class PygameEvents(metaclass=SingletonMeta):
    events: List[Event]
    def __init__(self) -> None:
        self.events = pygame.event.get()
    def update(self):
        self.events = pygame.event.get()


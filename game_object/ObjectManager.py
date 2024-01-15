from typing import List
from game_object.base.GameObject import GameObject
from singleton.SingletonMeta import SingletonMeta


class ObjectManager(metaclass=SingletonMeta):
    _game_objects: List[GameObject] = []

    def __init__(self) -> None:
        pass

    def attach(self, game_object:GameObject) -> None:
        self._game_objects.append(game_object)
        
    def detach(self, game_object:GameObject) -> None:
        self._game_objects.remove(game_object)
    
    def update(self) -> None:
        for observer in self._game_objects:
            observer.update()


    def get_objects(self) -> List[GameObject]:
        return self._game_objects

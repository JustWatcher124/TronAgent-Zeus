from typing import List
from game_object.base.GameObject import GameObject
from singleton.SingletonMeta import SingletonMeta


class ObjectManager(metaclass=SingletonMeta):
    _game_objects: List[GameObject]

    def __init__(self) -> None:
        self._game_objects = []

    def attach(self, game_object:GameObject) -> None:
        self._game_objects.append(game_object)
        
    def detach(self, game_object:GameObject) -> None:
        self._game_objects.remove(game_object)
    
    def update(self) -> None:
        for observer in self._game_objects:
            observer.update()

    def reset(self) -> None:
        self._game_objects = []

    def get_objects(self) -> List[GameObject]:
        return self._game_objects

object_manager = ObjectManager()

def InstantiateObject(game_object: GameObject) -> None:
    object_manager.attach(game_object)

def KillObject(game_object: GameObject) -> None:
    object_manager.detach(game_object)

def UpdateObjects() -> None:
    object_manager.update()

def GetObjects() -> List[GameObject]:
    return object_manager.get_objects()

def ResetObjectManager() -> None:
    object_manager.reset()

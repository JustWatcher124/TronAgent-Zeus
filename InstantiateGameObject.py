from game_object.ObjectManager import ObjectManager
from game_object.base.GameObject import GameObject

def InstantiateGameObject(game_object: GameObject):
    object_manager = ObjectManager()
    object_manager.attach(game_object)

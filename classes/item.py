from uuid import uuid4
from classes.player import Player

class Item:
    def __init__(self, properties: dict):
        if 'id' in properties.keys():
            self.id = properties['id']
        else:
            self.id = uuid4()
        self.name = properties['name']
        self.description = properties['description']
        self.type = properties['type']
        self.__dict__ = {
            **self.__dict__,
            **properties
        }
        self.func = self.define_action()

    def define_action(self):
        if self.type == 'miscellaneous':
            match self.effect:
                case 'heal':
                    return lambda: Player.heal(self.value)

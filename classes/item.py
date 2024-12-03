import pygame
import os

from config import *
from config.globalmanager import GlobalManager
from uuid import uuid4
from classes.player import Player

class Item(pygame.sprite.Sprite):
    def __init__(self, properties: dict, position: tuple = (0,0), *groups):
        super().__init__(*groups)

        self.id = uuid4()
        self.name = properties['name']
        self.description = properties['description']
        self.type = properties['type']
        self.item_id = properties['item_id']
        self.json_item = properties
        self.__dict__ = {
            **self.__dict__,
            **properties
        }

        if self.type == 'weapon' and 'equiped' not in self.__dict__:
            self.equiped = False

        self.func = self.define_action()

        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'items', properties['sprite'])),
            properties['scale']
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*MAP_SCALE_FACTOR
        self.rect.y = position[1]*MAP_SCALE_FACTOR
        self.original_rect: pygame.Rect = self.rect.copy()

    def define_action(self):
        if self.type == 'miscellaneous':
            match self.effect:
                case 'heal':
                    return lambda: Player.heal(self.value)

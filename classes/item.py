import pygame
import os

from config import *
from config.globalmanager import GlobalManager
from uuid import uuid4
from classes.player import Player

class Item(pygame.sprite.Sprite):
    def __init__(self, properties: dict, position: tuple = (0,0), tmx_item_id: int = None, *groups):
        super().__init__(*groups)

        self.id = uuid4()
        self.name = properties['name']
        self.description = properties['description']
        self.type = properties['type']
        self.item_id = properties['item_id']
        self.__dict__ = {
            **self.__dict__,
            **properties
        }
        self.tmx_item_id = tmx_item_id
        if 'tmx_item_id' in properties:
            self.tmx_item_id = properties['tmx_item_id']

        if self.type == 'weapon' and ('equiped' not in properties):
            self.equiped = False
            properties['equiped'] = False

        self.func = self.define_action()

        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'items', properties['sprite'])),
            properties['scale']
        )
        self.sprite_name = properties['sprite']
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

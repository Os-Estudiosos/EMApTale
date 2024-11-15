import pygame
import os

from config import *


class Vector(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'vector.png'))
        self.rect = self.image.get_rect()
    
    def update(self, *args, **kwargs):
        point_to_go = kwargs['player_center']

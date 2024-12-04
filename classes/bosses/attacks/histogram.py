import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

class Histogram(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Inicializando os sprites
        self.x_axis_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects','x_axis.png')
        self.y_axis_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects','y_axis.png')
        self.vasco_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects','vascao.png')
        self.x_axis = pygame.image.load(self.x_axis_path)
        self.y_axis = pygame.image.load(self.y_axis_path)
        self.vasco = pygame.image.load(self.vasco_path)

        # Inicializando os grupos
        self.bars_group = pygame.sprite.Group()
        self.axis_group = pygame.sprite.Group()

        # Adicinando no grupo global

    def update(self, *args, **kwargs):
        pass

    def randomize_bar(self):
        pass

    def draw_bars(self):
        pass

    def draw_axis(self):
        battle_container = CombatManager.get_variable('battle_container').out_rect
        battle_container_rect = battle_container.get_rect()

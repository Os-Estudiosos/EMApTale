import pygame
import os
import random
import math
import numpy as np

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

from classes.sprites.spritesheet import SpriteSheet


class Coffee(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Vou randomizar com 10% de chance de ser uma cobra cinza "Aplica o efeito de sumiço"
        self.type = 'Normal'
        if random.randint(0, 100) <= 15:
            self.type = 'Vanished'
        self.cup = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png'))
        self.smoke = SpriteSheet(rows=2, columns=13, image='smoke_coffee_sheet.png',frame_width=0, frame_heigth=0, x_offset=0, y_offset=0)
        self.counter = 0
        self.speed = 5
        SoundManager.play_sound('blade.wav')

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
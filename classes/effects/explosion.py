import pygame
import os

from config import *
from config.soundmanager import SoundManager

from classes.sprites.spritesheet import SpriteSheet


class Explosion(pygame.sprite.Sprite):
    def __init__(self, color: str, position: tuple[int], *groups):
        super().__init__(*groups)

        self.sprites = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', f'explosion-{color}.png'))

        self.scale = 2

        self.frames = SpriteSheet(
            1,
            7,
            self.sprites,
            31,
            31,
            3,
            0,
            self.scale
        )

        self.actual_frame = 0
        self.img = self.frames[0][self.actual_frame]
        self.rect = self.img.get_rect()
        self.rect.center = position
        self.finished = False
        self.counter = 0
    
    def update(self, *args, **kwargs):
        self.counter += 1
        if self.counter >= FPS*0.1:
            self.counter = 0
            self.actual_frame = self.actual_frame + 1
            if self.actual_frame >= len(self.frames[0]):
                self.finished = True
            else:
                self.img = self.frames[0][self.actual_frame]

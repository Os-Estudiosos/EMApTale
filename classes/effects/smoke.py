import pygame
import os

from config import *
from config.soundmanager import SoundManager

from classes.sprites.spritesheet import SpriteSheet


class Smoke(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int], *groups):
        super().__init__(*groups)

        self.smoke_sprites_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', '')
        self.cup = pygame.image.load(self.cup_path)
        self.smoke_sprites = pygame.image.load(self.smoke_sprites_path)
        self.smoke_frames = SpriteSheet(
            2,
            13,
            self.smoke_sprites,
            0,
            0,
            0,
            0,
            0
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

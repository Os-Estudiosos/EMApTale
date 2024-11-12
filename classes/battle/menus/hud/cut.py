import pygame
import os

from config import *
from config.soundmanager import SoundManager


class Cut(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.sprites: list[pygame.Surface] = [
        ]

        for i in range(6):
            self.sprites.append(
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', f'cut{i}.png')),
                    2
                )
            )

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

        self.frame_rate = FPS/5
        self.counter = 1
        self.animating = False
        self.frames_passed = 0
    
    def update(self, *args, **kwargs):
        self.counter += 1

        if self.animating and self.counter>=self.frame_rate:
            self.frames_passed += 1
            self.counter = 0
            if self.frames_passed >= len(self.sprites):
                self.animating = False
                self.counter = 1
                self.frames_passed = 0
            self.image = self.sprites[self.frames_passed]
            self.rect = self.image.get_rect()
            self.rect.centerx = pygame.display.get_surface().get_width()/2
            self.rect.centery = pygame.display.get_surface().get_height()/2-120
    
    def animate(self):
        self.animating = True
        self.frames_passed = 0
        self.counter = 1
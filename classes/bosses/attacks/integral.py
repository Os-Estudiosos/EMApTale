import pygame
import os

from config import *
from config.combatmanager import CombatManager


class Integral(pygame.sprite.Sprite):
    def __init__(self, dir, angle, *groups):
        super().__init__(*groups)

        self.display: pygame.Surface = pygame.display.get_surface()
        self.container = CombatManager.get_variable('battle_container')

        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image: pygame.Surface = pygame.transform.scale(
            self.image,
            (
                self.image.get_height(),
                self.container.inner_rect.width//2
            )
        )
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.dir = dir
        self.speed = 5

        self.rect.y = self.display.get_height()//2 + self.display.get_height()//2*dir
        self.rect.centerx = self.container.inner_rect.centerx + self.rect.width//2*dir

    def update(self, *args, **kwargs):
        self.rect.y += self.speed*self.dir*-1

import pygame
import os

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager


class Laugh(pygame.sprite.Sprite):
    def __init__(self, enemy, *groups):
        super().__init__(*groups)

        self.player = CombatManager.get_variable('player')
        self.enemy = enemy

        self.scale = 2
        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'laugh.png')),
            self.scale
        )
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.center = self.enemy.rect.center

        self.direction = pygame.math.Vector2(
            self.player.rect.x - self.rect.x,
            self.player.rect.y - self.rect.y
        )
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.speed = 5

        SoundManager.play_sound('branco_laugh.wav')

    def update(self, *args, **kwargs):
        self.rect.x += self.direction.x*self.speed
        self.rect.y += self.direction.y*self.speed

import pygame
import os
from random import choice
from config import *

from classes.battle.container import BattleContainer


class DamageBar(pygame.sprite.Sprite):
    def __init__(self, container: BattleContainer, groups: tuple[pygame.sprite.Group] = ()):
        super().__init__(*groups)

        self.sprites = [
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_bar_1.png')),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_bar_2.png'))
        ]
        for i in range(len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(
                self.sprites[i],
                (
                    self.sprites[i].get_width(),
                    container.inner_rect.height
                )
            )

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centery = container.inner_rect.centery
        self.rect.centerx = container.inner_rect.centerx

        self.random_dir = 0
        self.speed = 5

        self.animated = False

        self.execution_counter = 0
    
    def choose_direction(self):
        self.random_dir = choice([1, -1])

    def update(self, *args, **kwargs):
        # self.rect.x += self.speed * self.random_dir

        self.rect.x += self.speed*self.random_dir*-1

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
                    pygame.display.get_surface().get_height()*0.3
                )
            )

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

        self.container = container

        self.random_dir = 0
        self.speed = 10

        self.animated = False

        self.execution_counter = 0

    
    def choose_direction(self):
        self.random_dir = choice([1, -1])
        self.rect.centerx = self.container.inner_rect.centerx + (self.container.inner_rect.width/2)*self.random_dir
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_RETURN]:
            self.entered_pressing = True

    def update(self, *args, **kwargs):
        # self.rect.x += self.speed * self.random_dir

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_z] or keys[pygame.K_RETURN]) and not self.entered_pressing:
            self.random_dir = 0
            self.entered_pressing = True

        if not keys[pygame.K_RETURN] and not keys[pygame.K_z]:
            self.entered_pressing = False

        self.rect.x += self.speed*self.random_dir*-1
        self.rect.centery = self.container.inner_rect.centery

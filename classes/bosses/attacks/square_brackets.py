import pygame
import os

from config import *
from config.combatmanager import CombatManager


class SquareBracket(pygame.sprite.Sprite):
    def __init__(self, dir, *groups):
        super().__init__(*groups)

        self.container = CombatManager.get_variable('battle_container')

        self.dir = dir
        self.actual_alpha = 255
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'square_brackets.png')),
            (
                100,
                self.container.out_rect.height
            )
        )
        if dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_alpha(self.actual_alpha)
        self.rect = self.image.get_rect()

        self.rect.centerx = self.container.inner_rect.centerx
        self.rect.y = pygame.display.get_surface().get_height()

        self.animating = True

        self.animation_duration = FPS/1
        self.animation_counter = 0
    
    def update(self):
        self.animation_counter += 1

        if self.animating:
            direction = pygame.math.Vector2(
                (self.container.inner_rect.centerx + (self.container.inner_rect.width)*self.dir*-1) - self.rect.centerx,
                self.container.inner_rect.centery - self.rect.centery
            )

            if direction.length() <= 10:
                self.animating = False

            if direction.length() != 0:
                direction = direction.normalize()

            self.rect.x += direction.x*10
            self.rect.y += direction.y*10

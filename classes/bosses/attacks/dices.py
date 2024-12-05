import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager

from classes.sprites.spritesheet import SpriteSheet


class Dice(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.sprites = SpriteSheet(
            1,
            6,
            os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'dice.png'),
            16,
            16,
            scale_by=3
        )

        self.actual_sprite = 1

        self.image: pygame.Surface = self.sprites[0][self.actual_sprite]
        self.rect = self.image.get_rect()

        self.change_frame_rate = FPS/10
        self.change_frame_counter = 0

        self.gravity = 0.5
        self.force = 25

        self.dir = 0

        self.randomize_position()
    
    def randomize_position(self):
        container = CombatManager.get_variable('battle_container')

        self.dir = random.choice([1, -1])

        self.rect.x = random.randint(container.inner_rect.left, container.inner_rect.right)
        self.rect.y = pygame.display.get_surface().get_height()
    
    def change_sprites(self):
        self.image: pygame.Surface = self.sprites[0][self.actual_sprite]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.change_frame_counter += 1

        if self.change_frame_counter >= self.change_frame_rate:
            self.change_frame_counter = 0
            self.actual_sprite = (self.actual_sprite+1)%len(self.sprites[0])
            self.change_sprites()
        
        self.rect.x += (1*self.dir)

        self.rect.y -= self.force
        self.force -= self.gravity
        if self.force <= -10:
            self.force = -10

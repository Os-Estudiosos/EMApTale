import pygame
import os
import random
import math

from config import *
from config.combatmanager import CombatManager


class Vector(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Inicializo a imagem do vetor
        self.actual_alpha = 255
        self.image_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'vector.png')
        self.image = pygame.image.load(self.image_path)
        self.image.set_alpha(self.actual_alpha)
        self.rect = self.image.get_rect()
        self.randomize_position()

        self.fade_in_secs = FPS

        self.rotation_duration = FPS*0.5
        self.rotate_angle = 0
        self.max_rotation_angle = 180 * math.atan(
            (self.rect.centery - CombatManager.get_variable('player').rect.centery)/
            (self.rect.centerx - CombatManager.get_variable('player').rect.centerx)
        )

        self.counter = 0

    def fade_image(self):
        if self.counter <= 255:
            self.image.set_alpha(self.counter*(255/FPS))
    
    def rotate(self):
        print(self.max_rotation_angle)
        if self.rotate_angle < self.max_rotation_angle:
            self.rotate_angle += 1
            self.image = pygame.transform.rotate(
                pygame.image.load(self.image_path),
                self.rotate_angle
            )
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def randomize_position(self):
        battle_container = CombatManager.get_variable('battle_container')  # Pego o container
        display_rect = pygame.display.get_surface().get_rect()  # Pego a superfície da tela
        self.rect.x = random.randint(0, display_rect.width)  # Gero aleatoriamente dentro da tela
        self.rect.y = random.randint(0, display_rect.height)

        if self.rect.colliderect(battle_container.out_rect):  # Para sempre surgir fora do container
            self.rect.x += battle_container.out_rect.width * random.choice([1, -1])
            self.rect.y += battle_container.out_rect.height * random.choice([1, -1])

    def update(self, *args, **kwargs):
        self.counter += 1

        self.fade_image()

        self.rotate()

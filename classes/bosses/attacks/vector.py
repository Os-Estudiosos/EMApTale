import pygame
import os
import random
import math
import numpy as np
import time

from config import *
from config.combatmanager import CombatManager

from utils import radians_to_degrees, get_positive_angle, angle_between_vectors


class Vector(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Inicializo a imagem do vetor
        self.actual_alpha = 255
        self.image_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'vector.png')
        self.image = pygame.image.load(self.image_path)
        self.image.set_alpha(self.actual_alpha)
        self.mask = pygame.mask.from_surface(self.image)
        self.max_rotation_angle = 0
        self.rect = self.image.get_rect()
        self.randomize_position()

        self.fade_in_secs = FPS

        self.rotation_duration = FPS*0.5
        self.rotate_angle = 0
        self.rotating = True
        self.where_image_is_pointing = np.array([0, 1])
        self.player_rect = CombatManager.get_variable('player').rect.copy()
        self.vector_pointing_to_player = np.array([
            self.player_rect.centerx - self.rect.centerx,
            self.player_rect.centery - self.rect.centery
        ])
        self.max_rotation_angle = angle_between_vectors(self.where_image_is_pointing, self.vector_pointing_to_player)
        self.clockwise = False
        if self.rect.centerx >= self.player_rect.centerx:
            self.clockwise = True

        self.counter = 0

        self.speed = 7

    def fade_image(self):
        if self.counter <= 255:
            self.image.set_alpha(self.counter*(255/FPS))

    def rotate_image(self):
        self.image = pygame.transform.rotate(  # Rotaciono a imagem
            pygame.image.load(self.image_path),
            self.rotate_angle
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)  # Centralizo o retangulo no anterior

        # Rotacionando o vetor que indica para onde a flecha está apontando
        converted_angle = (self.rotate_angle*math.pi)/180
        
        rotation_matrix = np.array([
            [math.cos(converted_angle), -math.sin(converted_angle)],
            [math.sin(converted_angle), math.sin(converted_angle)]
        ])

        self.where_image_is_pointing = np.dot(rotation_matrix, self.where_image_is_pointing) / np.linalg.norm(self.where_image_is_pointing)

    def rotate(self):
        if self.rotating:
            if not self.clockwise:
                if self.rotate_angle <= self.max_rotation_angle:
                    self.rotate_angle += 5
                    self.rotate_image()
                else:
                    self.stop_rotating()
            elif self.clockwise:
                if -self.max_rotation_angle <= self.rotate_angle:
                    self.rotate_angle -= 5
                    self.rotate_image()
                else:
                    self.stop_rotating()
    
    def randomize_position(self):
        battle_container = CombatManager.get_variable('battle_container')  # Pego o container
        display_rect = pygame.display.get_surface().get_rect()  # Pego a superfície da tela
        self.rect.x = random.randint(30, display_rect.width-30)  # Gero aleatoriamente dentro da tela
        self.rect.y = random.randint(30, display_rect.height-30)

        if self.rect.colliderect(battle_container.out_rect):  # Para sempre surgir fora do container
            self.rect.x += battle_container.out_rect.width * random.choice([1, -1])
            self.rect.y += battle_container.out_rect.height * random.choice([1, -1])

    def update(self, *args, **kwargs):
        self.counter += 1

        if not self.rotating:
            self.rect.x += self.vector_pointing_to_player[0]*self.speed
            self.rect.y += self.vector_pointing_to_player[1]*self.speed
        
        self.rotate()
        self.fade_image()

    def stop_rotating(self):
        self.rotating = False
        self.vector_pointing_to_player = np.array([
            self.player_rect.centerx - self.rect.centerx,
            self.player_rect.centery - self.rect.centery
        ])
        self.vector_pointing_to_player = self.vector_pointing_to_player / np.linalg.norm(self.vector_pointing_to_player)

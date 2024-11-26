import pygame
import os

from config import *


class IntegralSword(pygame.sprite.Sprite):
    def __init__(self, initial_angle: int = 0, *groups):
        super().__init__(*groups)

        self.initial_angle = initial_angle

        self.scale = 10

        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, self.initial_angle)
        self.rect = self.image.get_rect()
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

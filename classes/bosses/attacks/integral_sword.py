import pygame
import os

from config import *


class IntegralSword(pygame.sprite.Sprite):
    def __init__(self, initial_angle: int = 0, *groups):
        super().__init__(*groups)

        self.initial_angle = initial_angle

        self.scale = 10

        self.moving = False

        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, self.initial_angle)
        self.rect = self.image.get_rect()
    
    def rotate_image_to(self, angle):
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def go_to(self, coordinate: tuple[int]):
        vector = pygame.math.Vector2(
            coordinate[0] - self.rect.centerx,
            coordinate[1] - self.rect.centery
        )

        if vector.length() > 10:
            vector = vector.normalize()

            self.rect.x += vector.x*5
            self.rect.y += vector.y*5
            self.moving = True
        else:
            self.moving = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

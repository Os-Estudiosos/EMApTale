import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame

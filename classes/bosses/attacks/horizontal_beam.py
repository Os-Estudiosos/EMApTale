import pygame
import random

from config import *
from config.combatmanager import CombatManager


class HorizontalBeam(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.rows = 4
        self.container = CombatManager.get_variable('battle_container')

        self.actual_display = pygame.display.get_surface()
        self.alpha = 255
        self.color = pygame.Color(255, 255, 255, self.alpha)

        self.image = pygame.Surface((self.actual_display.get_width(), self.container.inner_rect.height//self.rows), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.row = random.choice([i+1 for i in range(self.rows-1)])

        self.animating = True
        self.animation_counter = 0
        self.animation_duration = FPS

        self.correct_centery_position = self.container.inner_rect.y + (self.container.inner_rect.height//self.rows)*self.row - self.rect.height//2
    
    def fade_rect(self):
        self.alpha -= self.animation_counter
        if self.alpha < 0:
            self.alpha = 0
        self.color = pygame.Color(255, 255, 255, self.alpha)
        self.image.fill(self.color)
    
    def shrink_rect(self):
        if not self.rect.height - 10 < 0:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height-10))
            self.rect = self.image.get_rect()

    def update(self):
        self.animation_counter += 1

        if self.animating:            
            self.shrink_rect()
            self.fade_rect()
        
        self.rect.centery = self.correct_centery_position

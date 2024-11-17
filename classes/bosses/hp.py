import pygame

from config import *
from config.combatmanager import CombatManager


class BossHP:
    def __init__(self):
        self.life_rect = pygame.Rect(0,0,300,20)
        self.bg_rect = pygame.Rect(0,0,300,20)

        self.life_rect_color = pygame.Color(0, 255, 0)
        self.bg_rect_color = pygame.Color(50, 50, 50)
    
    def update(self, *args, **kwargs):
        enemy_rect = CombatManager.enemy.rect

        future_life_width = (kwargs['actual_life']*self.bg_rect.width)/kwargs['max_life']

        if self.life_rect.width >= future_life_width:
            self.life_rect.width -= 1 * FPS / 3


        self.bg_rect.center = enemy_rect.center
        self.bg_rect.centery += 40
        self.life_rect.topleft = self.bg_rect.topleft
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_rect_color, self.bg_rect)
        pygame.draw.rect(screen, self.life_rect_color, self.life_rect)

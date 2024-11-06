import pygame

from config.fontmanager import FontManager

from classes.player import Player
from classes.text.text import Text

class HPContainer:
    def __init__(self):
        self.out_color = pygame.Color(255, 255, 0)
        self.inner_color = pygame.Color(255, 0, 0)

        self.actual_player_hp = Player.life
        self.max_life = Player.max_life

        self.inner_rect = pygame.Rect(
            0,0,
            self.max_life*10,
            30
        )
        self.out_rect = self.inner_rect.copy()

        self.life_text = Text(f'{self.actual_player_hp}/{self.max_life}', FontManager.fonts['Gamer'], 45)
    
    def update(self):
        print(self.actual_player_hp)
        self.out_rect.topleft = self.inner_rect.topleft
        self.life_text.rect.topright = (
            self.inner_rect.topleft[0] - 40,
            self.inner_rect.topleft[1] -5
        )
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.inner_color, self.inner_rect)
        pygame.draw.rect(screen, self.out_color, self.out_rect)
        self.life_text.draw(screen)

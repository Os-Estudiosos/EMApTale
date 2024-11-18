import pygame
import os
from config import *
from classes.text.dynamic_text import DynamicText


class DialogueBox(pygame.sprite.Sprite):
    def __init__(self, text, font, letters_per_second, font_size, sound, *groups):
        super().__init__(*groups)

        self.text = text
        self.scale = 2
        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'dialogue', 'dialogue-bubble.png')),
            self.scale
        )
        self.rect = self.image.get_rect()
        self.text_rect_limiter = self.rect.copy()

        self.text_rect_limiter.width -= self.scale*42
        self.text_rect_limiter.height -= 20

        self.dynamic_text = DynamicText(text, font, letters_per_second, font_size, self.text_rect_limiter.width, sound=sound, color=(0,0,0))
    
    def update(self, *args, **kwargs):
        self.dynamic_text.position = self.text_rect_limiter.topleft
        self.text_rect_limiter.top = self.rect.top + 10
        self.text_rect_limiter.right = self.rect.right - 10
        self.dynamic_text.update()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (0,0,255),self.rect)
        # pygame.draw.rect(screen, (0,255,0),self.text_rect_limiter)
        self.dynamic_text.draw(screen)        

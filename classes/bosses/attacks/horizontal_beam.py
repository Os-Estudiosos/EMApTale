import pygame
import random
import math

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager


class HorizontalBeam(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.actual_display = pygame.display.get_surface()
        self.alpha = 0
        self.color = pygame.Color(255, 0, 0, self.alpha)

        self.max_rect_height = 0
        self.image = pygame.Surface((self.actual_display.get_width(), 10), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.update_mask()
        self.rect = self.image.get_rect()

        self.animating = False
        self.fading_counter = 0
        self.fading_duration = FPS/2
        self.appearing_counter = 0
        self.appearing_duration = FPS

        self.sound_counter = 0  # Evita do audio tocar sem parar

        self.correct_center_position = (0,0)
    
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def fade_out_rect(self):
        self.alpha -= self.fading_counter
        if self.alpha < 0:
            self.alpha = 0
        self.color = pygame.Color(255, 255, 255, self.alpha)
        self.image.fill(self.color)

    def fade_in_rect(self):
        self.alpha += self.fading_counter
        if self.alpha > 100:
            self.alpha = 100
        self.color = pygame.Color(255, 0, 0, self.alpha)
        self.image.fill(self.color)
    
    def shrink_rect(self):
        if not self.rect.height - 10 < 0:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height-10))
            self.rect = self.image.get_rect()
            self.update_mask()
    
    def grow_rect(self):
        if not self.rect.height + 10 > self.max_rect_height:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height+10))
            self.rect = self.image.get_rect()
            self.update_mask()

    def update(self):
        self.fading_counter += 1
        self.appearing_counter += 1

        if self.animating:
            if self.sound_counter == 0:
                self.sound_counter += 1
                SoundManager.stop_sound('sfx_segapower.wav')
                SoundManager.play_sound('sfx_rainbowbeam.wav')
            self.shrink_rect()
            self.fade_out_rect()
        else:
            if self.sound_counter == 0:
                self.sound_counter += 1
                SoundManager.play_sound('sfx_segapower.wav')
            self.grow_rect()
            self.fade_in_rect()
            if self.alpha == 100 and self.appearing_counter >= self.appearing_duration//2:
                self.fading_counter = 0
                self.sound_counter = 0
                self.alpha = 255
                self.animating = True
        
        self.rect.center = self.correct_center_position

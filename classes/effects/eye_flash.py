import pygame
import os

from config import *
from config.soundmanager import SoundManager

from classes.sprites.spritesheet import SpriteSheet


class EyeFlash(pygame.sprite.Sprite):
    def __init__(self, dir, type, *groups):
        super().__init__(*groups)

        self.dir = dir
        self.sprites = SpriteSheet(
            1,
            6,
            os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'eye_flashes.png'),
            13,
            13,
            5,
            0,
            3
        )

        self.frame_change_rate = FPS/20
        self.frame_change_counter = 0
        self.animating = True

        self.actual_sprite = 0
        self.image: pygame.Surface = self.sprites[0][self.actual_sprite]
        self.rect = self.image.get_rect()

        for i in range(len(self.sprites[0])):
            color_surface = pygame.Surface(self.rect.size)
            color_surface.fill((5, 153, 245) if type=='stop' else (255, 145, 0))
            self.sprites[0][i].blit(color_surface, (0,0), special_flags=pygame.BLEND_RGB_MULT)
        
        SoundManager.play_sound('eyeflash.wav')

    def update(self, *args, **kwargs):
        self.frame_change_counter += 1

        if self.frame_change_counter >= self.frame_change_rate and self.animating:
            if self.actual_sprite+1 >= len(self.sprites[0]):
                self.animating = False
            
            self.image = self.sprites[0][self.actual_sprite%(len(self.sprites[0]))]

            self.frame_change_counter = 0
            self.actual_sprite += 1
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

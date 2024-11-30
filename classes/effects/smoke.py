import pygame
import os

from config import *
from config.soundmanager import SoundManager
from classes.sprites.spritesheet import SpriteSheet


class Smoke(pygame.sprite.Sprite):
    def __init__(self, *groups, fps=60):
        super().__init__(*groups)

        # Inicializando o caminho para o spritesheet de fumaça
        self.smoke_sprites_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'smoke_animation_sheet.png')

        # Carregando o spritesheet
        self.smoke_sprites = pygame.image.load(self.smoke_sprites_path).convert_alpha()

        # Criando os frames a partir do SpriteSheet
        self.smoke_frames = SpriteSheet(
            rows=2,
            columns=13,
            image=self.smoke_sprites,
            frame_width=63,
            frame_heigth=80,
            x_offset=0,
            y_offset=0,
            scale_by=1
        )

        self.actual_frame = 0
        self.image = self.smoke_frames[0][self.actual_frame]  # Inicializa o quadro atual
        self.rect = self.image.get_rect()  # Define a área do sprite
        self.finished = False
        self.counter = 0
        self.fps = fps
        SoundManager.play_sound('blade.wav')

    def update(self, *args, **kwargs):
        # Incrementa o contador para controlar o tempo entre os quadros
        self.counter += 1
        if self.counter >= self.fps * 0.1:  # Ajusta o tempo baseado nos FPS
            self.counter = 0
            self.actual_frame += 1

            # Verifica se a animação terminou
            if self.actual_frame >= len(self.smoke_frames[0]):
                self.finished = True
            else:
                # Atualiza a imagem com o próximo quadro
                self.image = self.smoke_frames[0][self.actual_frame]

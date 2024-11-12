import pygame
import os

from config import *
from config.soundmanager import SoundManager


class Cut(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Lista com meus sprites
        self.sprites: list[pygame.Surface] = [
        ]

        # Adiciono dinamicamente meus sprites (Todos tem nomes parecidos 'cut{i}.png')
        for i in range(6):
            self.sprites.append(
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', f'cut{i}.png')),
                    2.4
                )
            )

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

        self.position = (
            pygame.display.get_surface().get_width()/2,
            pygame.display.get_surface().get_height()/2-150
        )

        self.frame_rate = FPS/5  # Taxa de frames por segundo da animação
        self.animation_counter = 1  # Contador da animação
        self.animating = False  # Se a animação está rodando
        self.frames_passed = 0  # Qual o frame atual da animação
        self.can_animate_again = False
    
    def update(self, *args, **kwargs):
        self.animation_counter += 1  # Adiciono ao contador da animação

        # Se a animação estiver rodando e meu contador for maior que a taxa de quadros por segundo
        if self.animating and self.animation_counter>=self.frame_rate and self.can_animate_again:
            self.frames_passed += 1  # Aumento o frame
            self.animation_counter = 0  # Zero o contador da animação
            if self.frames_passed >= len(self.sprites):  # Se o frame for maior que a quantidade de sprites
                self.animating = False  # Paro a animação
                self.animation_counter = 1  # Coloco o contador para 1
                self.frames_passed = 0  # Reinicio a minha animação
                self.can_animate_again = False
            self.image = self.sprites[self.frames_passed]  # Mudo o sprite atual
            self.rect = self.image.get_rect()  # Pego o retangulo
        # Centralizo
        self.rect.center = self.position
    
    def animate(self):
        """Método que indica que eu tenho que começar a animação
        """
        self.animating = True  # Coloco para a animação começar a rodar
        self.frames_passed = 0
        self.animation_counter = 1
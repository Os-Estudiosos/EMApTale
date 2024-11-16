import pygame
import os

from config import *
from config.soundmanager import SoundManager
from config.combatmanager import CombatManager

from constants import BOSS_HITTED


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
            0,
            0
        )

        self.frame_rate = FPS/5  # Taxa de frames por segundo da animação
        self.animation_counter = 1  # Contador da animação
        self.__animating = False  # Se a animação está rodando
        self.frames_passed = 0  # Qual o frame atual da animação
    
    def update(self, *args, **kwargs):
        self.animation_counter += 1  # Adiciono ao contador da animação
        self.position = (
            CombatManager.enemy.rect.centerx,
            CombatManager.enemy.rect.centery
        )

        # Se a animação estiver rodando e meu contador for maior que a taxa de quadros por segundo
        if self.animation_counter>=self.frame_rate and self.__animating:
            self.frames_passed += 1  # Aumento o frame
            self.animation_counter = 0  # Zero o contador da animação
            if self.frames_passed >= len(self.sprites):  # Se o frame for maior que a quantidade de sprites
                self.__animating = False  # Paro a animação
                self.animation_counter = 1  # Coloco o contador para 1
                self.frames_passed = 0  # Reinicio a minha animação
                self.can_animate_again = False
                pygame.event.post(pygame.event.Event(BOSS_HITTED))
            self.image = self.sprites[self.frames_passed]  # Mudo o sprite atual
            self.rect = self.image.get_rect(center=self.position)  # Pego o retangulo
    
    def animate(self):
        """Método que indica que eu tenho que começar a animação
        """
        self.__animating = True
        self.frames_passed = 0
        self.animation_counter = 1

    @property
    def animating(self):
        return self.__animating

    @animating.setter
    def animating(self, value: bool):
        self.__animating = value

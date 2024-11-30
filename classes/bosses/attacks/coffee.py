import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

from classes.effects.smoke import Smoke


class Coffee(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        """
        Representa uma xícara de café com vapor animado.
        
        Args:
            x (int): Coordenada x da posição inicial da xícara.
            y (int): Coordenada y da posição inicial da xícara.
            groups (pygame.sprite.Group): Grupos aos quais o sprite pertence.
        """
        super().__init__(*groups)

        # Carregando o sprite da xícara
        self.cup_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png')
        self.image = pygame.image.load(self.cup_path).convert_alpha()  # Define `self.image` esperado pelo Pygame
        self.rect = self.image.get_rect(center=(x, y))  # Define `self.rect` com a posição inicial

        # Inicializando o efeito de fumaça
        self.smoke = Smoke()
        self.smoke.rect.midbottom = self.rect.midtop  # Alinha a fumaça com o topo da xícara
        self.smoke_group = pygame.sprite.Group(self.smoke)

    def update(self, *args, **kwargs):
        """
        Atualiza o estado da xícara e anima o vapor.
        """
        # Atualiza a posição da fumaça para alinhar com a xícara
        self.smoke.rect.midbottom = self.rect.midtop

        # Atualiza a fumaça
        self.smoke_group.update()

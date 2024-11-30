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
        self.image = pygame.transform.scale(pygame.image.load(self.cup_path), (100,100)).convert_alpha()  # Define `self.image` esperado pelo Pygame
        self.cup_bottom = CombatManager.get_variable('battle_container').inner_rect.bottom
        self.rect = self.image.get_rect(center=(x, y))  # Define `self.rect` com a posição inicial
        self.rect.bottom = self.cup_bottom
        self.player = CombatManager.get_variable('player')
        self.boss = CombatManager.enemy
        

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
        if pygame.sprite.spritecollide(self.player, self.smoke_group, True, pygame.sprite.collide_mask):
            self.player.take_damage(self.boss.damage)
    


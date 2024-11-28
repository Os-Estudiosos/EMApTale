import pygame
import os
import random
import math
import numpy as np

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

from classes.sprites.spritesheet import SpriteSheet
from classes.effects.smoke import Smoke


class Coffee(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Vou randomizar com 10% de chance de "aplicar o efeito de sumiço"
        self.type = 'Normal'
        if random.randint(0, 100) <= 15:
            self.type = 'Vanished'

        # Inicializando os sprites da xícara e do vapor de café
        self.cup_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png')
        '''Pegar a classe Smoke para fazer a animação do vapor'''
        self.rect = self.cup.get_rect()

        # Pegando o retângulo do player
        self.player_rect = CombatManager.get_variable('player').rect.copy()

        # Iniciando variáveis gerais de turno e som
        self.counter = 0
        self.speed = 5
        SoundManager.play_sound('blade.wav')

    def update(self, *args, **kwargs):
        self.counter += 1
        battle_container = CombatManager.get_variable('battle_container')
        display_surface_rect = pygame.display.get_surface().get_rect()
        
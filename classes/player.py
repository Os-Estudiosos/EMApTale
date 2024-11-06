import pygame
from time import time

from config.savemanager import SaveManager
from config.soundmanager import SoundManager


class Player(pygame.sprite.Sprite):
    # Definindo as variáveis do Player
    inventory = []
    life = 0
    max_life = 0
    name = ''
    last_hit = 0

    # Carregando sa informações do Player
    @classmethod
    def load_infos(cls):
        """Classe responsável por carregar as informações do personagem
        """
        cls.name = SaveManager.loaded_save['name']
        cls.life = SaveManager.loaded_save['player']['life']
        cls.max_life = SaveManager.loaded_save['player']['max_life']
        cls.inventory = SaveManager.loaded_save['inventory']

    @classmethod
    def take_damage(cls, value: int):
        """Subtrai o valor passado da vida do jogador

        Args:
            value (int): Valor do dano
        """
        actual_hit = time()
        if actual_hit - cls.last_hit >= 2:  # Aqui eu dou um delay de 1 segundo para dar dano
            cls.life -= value
            cls.last_hit = actual_hit
            SoundManager.play_sound('hurt.wav')
    
    @classmethod
    def heal(cls, value: int):
        """Curo a vida do player

        Args:
            value (int): Valor da cura
        """
        cls.life += value

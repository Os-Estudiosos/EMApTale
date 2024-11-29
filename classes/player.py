import pygame
from time import time

from config.savemanager import SaveManager
from config.soundmanager import SoundManager

from classes.inventory import Inventory


class Player(pygame.sprite.Sprite):
    # Definindo as variáveis do Player
    inventory = Inventory()
    level = 1
    life = 0
    max_life = 0
    name = ''
    last_hit = 0

    # Carregando sa informações do Player
    @classmethod
    def load_infos(cls):
        """Classe responsável por carregar as informações do personagem
        """
        Player.name = SaveManager.loaded_save['name']
        Player.life = SaveManager.loaded_save['player']['life']
        Player.max_life = SaveManager.loaded_save['player']['max_life']
        Player.inventory = Inventory(SaveManager.loaded_save['inventory'])

    @classmethod
    def take_damage(cls, value: int):
        """Subtrai o valor passado da vida do jogador

        Args:
            value (int): Valor do dano
        """
        actual_hit = time()
        if actual_hit - Player.last_hit >= 0.5:  # Aqui eu dou um delay de 1 segundo para dar dano
            if Player.life - value >= 0:
                Player.life -= value
            else:
                Player.life = 0
            Player.last_hit = actual_hit
            SoundManager.play_sound('hurt.wav')
    
    @classmethod
    def heal(cls, value: int):
        """Curo a vida do player

        Args:
            value (int): Valor da cura
        """
        if Player.life == Player.max_life:
            return False
        elif Player.life + value >= Player.max_life:
            Player.life = Player.max_life
            SoundManager.play_sound('heal.wav')
        else:
            Player.life += value
            SoundManager.play_sound('heal.wav')
        return True

import pygame

from config.savemanager import SaveManager


class Player(pygame.sprite.Sprite):
    # Definindo as variáveis do Player
    inventory = []
    life = 0

    # Carregando sa informações do Player
    def __new__(cls, *args, **kwargs):

        cls.life = SaveManager.loaded_save['player']['life']
        cls.inventory = SaveManager.loaded_save['inventory']

        return super().__new__(cls)

    def __init__(self, *groups):
        super().__init__(*groups)

    @classmethod
    def take_damage(cls, value: int):
        """Subtrai o valor passado da vida do jogador

        Args:
            value (int): Valor do dano
        """
        cls.life -= value
    
    @classmethod
    def heal(cls, value: int):
        """Curo a vida do player

        Args:
            value (int): Valor da cura
        """
        cls.life += value

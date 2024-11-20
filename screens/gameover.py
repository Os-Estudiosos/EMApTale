import pygame
from screens import State

from config import *

from classes.battle.button import CombatButton
from classes.battle.container import BattleContainer
from classes.battle.hp_container import HPContainer

from classes.text.dynamic_text import DynamicText
from classes.text.text import Text

from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager

from classes.battle.heart import Heart
from classes.player import Player

class GameOver(State):
    def __init__(
            self, 
            name:str, 
            display:pygame.Surface,
            game_state_manager:GameStateManager
            ):
        
        # Variáveis padrão de qualquer Cenário
        self.__name = name
        self.__display: pygame.Surface = display
        self.__game_state_manager: GameStateManager = game_state_manager
        #self.execution_counter = 0

    # @property
    # def execution_counter(self):
    #     return self.execution_counter

    @property
    def display(self):
        return self.display
    
    @property
    def game_state_manager(self):
        return self.__game_state_manager
    
    @property
    def name(self):
        return self.__name
    
    def heart_break(self):
        pass

    def heart_pieces(self):
        pass
    
    def on_first_execution(self):
        # Limpando os sons
        pass
    
    def run(self):
        pass

    def on_last_execution(self):
        self.__execution_counter = 0


'''
on_first_execution:
Tiro os sons
Deixo só o personagem

run:
Executo a função de heart_break (substituo o sprite do coração e toco a música heart_break)
Executo a função heart_pieces (subsituo pelas partículas do coração e toco a música heart_pieces)
Mudo para a cena do Game Over e toco a música 
Coloco uma caixa de texto

on_last_execution:
Volto para o menu principal
Depois vamos ver se conseguimos fazer o personagem voltar para onde ele
'''
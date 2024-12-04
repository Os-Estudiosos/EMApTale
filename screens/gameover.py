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
            display:pygame.Surface
            ):
        
        # Variáveis padrão de qualquer Cenário
        self.__name = name
        self.__display: pygame.Surface = display
        #self.execution_counter = 0

    # @property
    # def execution_counter(self):
    #     return self.execution_counter

    @property
    def display(self):
        return self.display
    
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

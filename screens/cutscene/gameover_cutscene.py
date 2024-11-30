import pygame
import os
from screens import State

from config import *
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

class GameoverCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0
        self.__variables = {}   

    def on_first_execution(self):
        pass

    def run(self):
        # Chama o que será executado apenas na primeira vez
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
            self.__game_state_manager.set_state("intro_cutscene")
        

    def on_last_execution(self):    
        self.__execution_counter = 0
        SoundManager.play_music

    @property
    def execution_counter(self):
        return self.execution_counter


    @property
    def display(self):
        return self.display


    @property
    def name(self):
        return self.__name    


    @property
    def game_state_manager(self):
        return self.__game_state_manager

    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value

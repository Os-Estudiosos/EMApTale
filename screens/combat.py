import pygame
from screens import State
from config import *

from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager


class Combat(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        sound_manager: SoundManager,
        game_state_manager: GameStateManager,
        font_manager: FontManager
    ):
        # Variáveis padrão de qualquer Cenário
        self.__name = name
        self.__display: pygame.Surface = display
        self.__sound_manager: SoundManager = sound_manager
        self.__game_state_manager: GameStateManager = game_state_manager
        self.__font_manager: FontManager = font_manager

        self.__execution_counter = 0
    
    def on_first_execution(self):
        # Limpando os sons
        self.__sound_manager.stop_music()

    def run(self):
        self.__display.fill((255,255,255))

        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
    
    def on_last_execution(self):
        self.__execution_counter = 0

    @property
    def execution_counter(self):
        return self.execution_counter

    @property
    def display(self):
        return self.display
    
    @property
    def sound_manager(self):
        return self.__sound_manager
    
    @property
    def game_state_manager(self):
        return self.__game_state_manager
    
    @property
    def font_manager(self):
        return self.__font_manager
    
    @property
    def name(self):
        return self.__name
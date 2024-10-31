import pygame
from screens import State
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager


class Menu(State):
    def __init__(self, name: str, display: pygame.Surface, sound_manager: SoundManager, game_state_manager: GameStateManager):
        self.__name = name
        self.__display: pygame.Surface = display
        self.__sound_manager: SoundManager = sound_manager
        self.__game_state_manager: GameStateManager = game_state_manager

    def run(self):
        self.__display.fill((255, 0, 0))

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
    def name(self):
        return self.__name

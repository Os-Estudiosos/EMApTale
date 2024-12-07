import pygame
import time
from screens import State

from config import *

from classes.text.text import Text

from config.soundmanager import SoundManager
from config.fontmanager import FontManager
from config.gamestatemanager import GameStateManager
from config.globalmanager import GlobalManager

from constants import *


class ShowDayCutscene(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display

        self.__execution_counter = 0

        self.day_text = None

        self.state_id = 0

        self.transition_from_text_to_black_screen_ticks = 0
        self.transition_from_black_screen_to_game_ticks = 0

    def on_first_execution(self):
        SoundManager.play_sound('intro_noise.ogg')
        self.__execution_counter += 1
        self.state_id = 0
        self.day_text = Text(f'DIA {GlobalManager.day+1}', FontManager.fonts['Gamer'], int(self.__display.get_height() * 0.4))
        self.day_text.rect.center = self.__display.get_rect().center
        self.transition_from_text_to_black_screen_ticks = time.time()

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()

        actual_tick = time.time()

        if actual_tick - self.transition_from_text_to_black_screen_ticks > 3 and self.state_id == 0:
            SoundManager.play_sound('intro_noise.ogg')
            self.state_id += 1
            self.transition_from_black_screen_to_game_ticks = time.time()
        
        if actual_tick - self.transition_from_black_screen_to_game_ticks > 2 and self.state_id == 1:
            GameStateManager.set_state('emap')

        if self.state_id != 1:
            self.day_text.draw(self.__display)

    def on_last_execution(self):
        self.__execution_counter = 0

    @property
    def execution_counter(self):
        return self.__execution_counter

    @property
    def display(self):
        return self.__display
    
    @property
    def name(self):
        return self.__name

    @property
    def variables(self):
        return self.__variables
    
    @variables.setter
    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value

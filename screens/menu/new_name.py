import pygame
import os
from screens import State

from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.savemanager import SaveManager
from config.eventmanager import EventManager

from classes.text.text import Text


class NewName(State):
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

        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.player_name = ''
        self.font_size = 60
        self.max_player_name_size = 10
        self.player_name_text = Text('', FontManager.fonts['Gamer'], self.font_size)
    
    def on_first_execution(self):
        # Checo se ele não iniciou a cena segurando o botão de confirmar
        EventManager.clear()

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
        
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if len(self.player_name) <= self.max_player_name_size:
                    if 97 <= event.key <= 122:
                        self.player_name+=self.letters[event.key - 97]
                    if event.key == pygame.K_SPACE and len(self.player_name) <= 30:
                        self.player_name += ' '
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[0:len(self.player_name)-1]
                
                self.player_name_text = Text(self.player_name, FontManager.fonts['Gamer'], self.font_size)

                if event.key == pygame.K_RETURN and len(self.player_name)>0:
                    SaveManager.create_new_save_file(self.player_name)
                    GameStateManager.set_state('intro_cutscene')
        
        set_your_name_text = Text('DIGITE O SEU NOME', FontManager.fonts['Gamer'], self.font_size)
        confirm_text = Text('APERTE ENTER PARA CONFIRMAR', FontManager.fonts['Gamer'], self.font_size - 30)

        self.player_name_text.rect.centerx = self.__display.get_rect().width/2
        self.player_name_text.rect.centery = self.__display.get_rect().height/2

        set_your_name_text.rect.center = self.player_name_text.rect.center
        set_your_name_text.rect.centery -= 50

        confirm_text.rect.center = self.player_name_text.rect.center
        confirm_text.rect.centery += 50

        self.player_name_text.draw(self.display)
        set_your_name_text.draw(self.display)
        confirm_text.draw(self.display)

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

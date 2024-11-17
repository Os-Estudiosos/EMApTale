import pygame
import os
import time
from screens import State
from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.eventmanager import EventManager

from classes.text.text import Text


class Start(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        game_state_manager: GameStateManager,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display
        self.__game_state_manager: GameStateManager = game_state_manager

        self.__execution_counter = 0

        # Opções do Menu
        self.menu_options = [
            {
                'label': Text('NOVO JOGO', FontManager.fonts['Gamer'], 50),
                'func': lambda: self.__game_state_manager.set_state('new_game_confirmation')
            },
            {
                'label': Text('CONTINUAR JOGO', FontManager.fonts['Gamer'], 50),
                'func': lambda: self.__game_state_manager.set_state('emap')
            },
            # {
            #     'label': Text('OPÇÕES', FontManager.fonts['Gamer'], 50),
            #     'func': lambda: self.__game_state_manager.set_state('options')
            # },
            {
                'label': Text('SAIR', FontManager.fonts['Gamer'], 50),
                'func': lambda: pygame.quit()
            }
        ]
        self.selected_option = 0  # Opção que está selecionada
        self.option_measures = [500, 105]  # Medidas de cada Opção
        self.display_info = pygame.display.Info()  # Informações sobre a tela

        # Informações sobre o cursor que marca qual a opção selecionada
        self.cursor_icon = pygame.transform.scale_by(pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')), 1.5)
        self.cursor_rect = self.cursor_icon.get_rect()
    
    def on_first_execution(self):
        # Inicializando a Música
        if not SoundManager.is_playing():
            SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), 'sounds', 'msc_the_field_of_dreams.mp3'))

        # Checo se ele não iniciou a cena segurando o botão de confirmar
        EventManager.clear()

    def move_cursor(self, increment):
        if self.selected_option + increment >= len(self.menu_options):
            self.selected_option = 0
        elif self.selected_option + increment < 0:
            self.selected_option = len(self.menu_options)-1
        else:
            self.selected_option += increment

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Se eu apertar pra baixo
                    self.move_cursor(1)  # Movo uma opção pra baixo
                    self.cursor_trying_to_move = True
                    SoundManager.play_sound('squeak.wav')
                elif event.key == pygame.K_UP:  # Se eu apertar para cima
                    self.move_cursor(-1)  # Movo uma opção pra cima
                    self.cursor_trying_to_move = True
                    SoundManager.play_sound('squeak.wav')

                if event.key == pygame.K_z or event.key == pygame.K_RETURN:  # Se eu apertar enter em alguma opção
                    self.menu_options[self.selected_option]['func']()
                    SoundManager.play_sound('select.wav')

        self.cursor_rect.center = (  # Mexo o centro do cursor
            self.menu_options[self.selected_option]['label'].rect.center[0] + 300,  # Matemática para mexer o cursor
            self.menu_options[self.selected_option]['label'].rect.center[1]  # Centralizando o cursor
        )

        # Desenho cada uma das opções
        for i, option in enumerate(self.menu_options):
            # Matemática para centralizar as opções
            option['label'].rect.center = (
                self.display_info.current_w/2,
                (self.option_measures[1]/2) + (self.option_measures[1]*(i)) + (self.display_info.current_h-self.option_measures[1]*len(self.menu_options))/2,
            )
            
            # Desenhando o texto da opção
            option['label'].draw(self.__display)
        
        self.__display.blit(self.cursor_icon, self.cursor_rect)

    def on_last_execution(self):
        self.__execution_counter = 0

    @property
    def execution_counter(self):
        return self.execution_counter

    @property
    def display(self):
        return self.display
    
    @property
    def game_state_manager(self):
        return self.__game_state_manager
    
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

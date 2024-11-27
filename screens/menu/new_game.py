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
        
class NewGameConfirmation(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface
    ):
        # Variáveis padrão de qualquer Cenário
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display

        self.__execution_counter = 0

        self.menu_options = [
            {
                'label': Text('SIM', FontManager.fonts['Gamer'], 50),
                'func': lambda: GameStateManager.set_state('new_name')
            },
            {
                'label': Text('CANCELAR', FontManager.fonts['Gamer'], 50),
                'func': lambda: GameStateManager.set_state('start')
            }
        ]
        self.selected_option = 0  # Opção que está selecionada
        self.option_measures = [220, 105]  # Medidas de cada Opção
        self.display_info = pygame.display.Info()  # Informações sobre a tela

        # Informações sobre o cursor que marca qual a opção selecionada
        self.cursor_icon = pygame.transform.scale_by(pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')), 1.5)
        self.cursor_rect = self.cursor_icon.get_rect()
    
    def on_first_execution(self):
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

        # Fazendo o texto de confirmação
        text_confirmation = ''
        if SaveManager.save_exists():
            text_confirmation = 'Deseja sobrescrever seu progresso com um novo jogo?'
        else:
            GameStateManager.set_state('new_name')
        text_object = Text(text_confirmation, FontManager.fonts['Gamer'], 60)
        text_object.rect.center = (
            self.__display.get_width()/2,
            self.__display.get_height()/2-60
        )

        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Se eu apertar pra baixo
                    self.move_cursor(1)  # Movo uma opção pra baixo
                    self.cursor_trying_to_move = True
                    SoundManager.play_sound('squeak.wav')
                elif event.key == pygame.K_LEFT:  # Se eu apertar para cima
                    self.move_cursor(-1)  # Movo uma opção pra cima
                    self.cursor_trying_to_move = True
                    SoundManager.play_sound('squeak.wav')

                if event.key == pygame.K_z or event.key == pygame.K_RETURN:  # Se eu apertar enter em alguma opção
                    self.menu_options[self.selected_option]['func']()
                    SoundManager.play_sound('select.wav')
        
        # Ajustando o cursor
        self.cursor_rect.topleft = self.menu_options[self.selected_option]['label'].rect.topright

        # Desenho cada uma das opções
        for i, option in enumerate(self.menu_options):
            # Matemática para centralizar as opções
            option['label'].rect.center = (
                # self.display_info.current_w/2,
                # (self.option_measures[1]/2) + (self.option_measures[1]*(i)) + (self.display_info.current_h-self.option_measures[1]*len(self.menu_options))/2,
                (self.option_measures[0]/2) + (self.option_measures[0]*(i)) + (self.display_info.current_w-self.option_measures[0]*len(self.menu_options))/2,
                self.display_info.current_h/2,
            )
            
            # Desenhando o texto da opção
            option['label'].draw(self.__display)
        
        self.__display.blit(self.cursor_icon, self.cursor_rect)
        text_object.draw(self.__display)

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
        

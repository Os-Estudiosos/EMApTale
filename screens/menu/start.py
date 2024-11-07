import pygame
import os
import time
from screens import State
from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager

from classes.text.text import Text


class Start(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        game_state_manager: GameStateManager,
    ):
        # Variáveis padrão de qualquer Cenário
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
        self.cursor_trying_to_move = False  # Marca se eu estou tentando mexer o cursor

        # Essa variável é responsável por checar se o player entrou na cena com o botão
        # de confirmação selecionado (Enter ou Z), assim eu posso evitar que ele entre
        # na tela ja selecionando a opção por acidente
        self.entered_holding_confirm_button = False
    
    def on_first_execution(self):
        # Inicializando a Música
        if not SoundManager.is_playing():
            SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), 'sounds', 'msc_the_field_of_dreams.mp3'))

        # Checo se ele não iniciou a cena segurando o botão de confirmar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_z]:
            self.entered_holding_confirm_button = True

    def move_cursor(self, increment):
        if self.selected_option + increment >= len(self.menu_options):
            self.selected_option = 0
        elif self.selected_option + increment < 0:
            self.selected_option = len(self.menu_options)-1
        else:
            self.selected_option += increment

    def run(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and not self.cursor_trying_to_move:  # Se eu apertar pra baixo
            self.move_cursor(1)  # Movo uma opção pra baixo
            self.cursor_trying_to_move = True
            SoundManager.play_sound('select.wav')
        elif keys[pygame.K_UP] and not self.cursor_trying_to_move:  # Se eu apertar para cima
            self.move_cursor(-1)  # Movo uma opção pra cima
            self.cursor_trying_to_move = True
            SoundManager.play_sound('select.wav')

        if (keys[pygame.K_z] or keys[pygame.K_RETURN]) and not self.entered_holding_confirm_button:  # Se eu apertar enter em alguma opção
            self.menu_options[self.selected_option]['func']()
        
        # Se ele estiver segurando o botão quando entrou na cena, ao soltar, podera clicar nas opções
        if not keys[pygame.K_z] and not keys[pygame.K_RETURN]:
            self.entered_holding_confirm_button = False
        
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            # Só deixo mover o cursor se eu soltar a tecla e apertar de novo
            self.cursor_trying_to_move = False

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
    def game_state_manager(self):
        return self.__game_state_manager
    
    @property
    def name(self):
        return self.__name

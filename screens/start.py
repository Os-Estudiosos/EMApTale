import pygame
import os
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

        # Opções do Menu
        self.menu_options = [
            {
                'label': Text('NOVO JOGO', self.__font_manager.fonts['Gamer'], 50)
            },
            {
                'label': Text('CARREGAR JOGO', self.__font_manager.fonts['Gamer'], 50)
            },
            {
                'label': Text('OPÇÕES', self.__font_manager.fonts['Gamer'], 50)
            },
            {
                'label': Text('SAIR', self.__font_manager.fonts['Gamer'], 50),
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
    
    def on_first_execution(self):
        # Inicializando a Música
        self.__sound_manager.play_music(os.path.join(GET_PROJECT_PATH(), 'sounds', 'the_field_of_dreams.mp3'))
        self.__sound_manager.load_sound_list([
            os.path.join(GET_PROJECT_PATH(), 'sounds', 'select.wav')
        ])

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
            self.__sound_manager.play_sound('select.wav')
        elif keys[pygame.K_UP] and not self.cursor_trying_to_move:  # Se eu apertar para cima
            self.move_cursor(-1)  # Movo uma opção pra cima
            self.cursor_trying_to_move = True
            self.__sound_manager.play_sound('select.wav')

        if keys[pygame.K_z] or keys[pygame.K_RETURN]:  # Se eu apertar enter em alguma opção
            self.menu_options[self.selected_option]['func']()
        
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # Se eu n tiver tentando mexer
            self.cursor_trying_to_move = False

        self.cursor_rect.center = (  # Mexo o centro do cursor
            self.menu_options[self.selected_option]['label'].rect.center[0] + 300,
            self.menu_options[self.selected_option]['label'].rect.center[1]
        )

        # Desenho cada uma das opções
        for i, option in enumerate(self.menu_options):
            option['label'].rect.center = (
                self.display_info.current_w/2,
                (self.option_measures[1]/2) + (self.option_measures[1]*(i)) + (self.display_info.current_h-self.option_measures[1]*len(self.menu_options))/2,
            )
            
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

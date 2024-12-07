import pygame
import os

from screens import State
from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.eventmanager import EventManager
from config.globalmanager import GlobalManager
from config.savemanager import SaveManager

from classes.text.text import Text


class PauseMenu(State):
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

        # Opções do Menu
        self.menu_options = [
            {
                'label': Text('CONTINUAR JOGO', FontManager.fonts['Gamer'], 50),
                'func': lambda: GlobalManager.resume()
            },
            {
                'label': Text('SALVAR O JOGO', FontManager.fonts['Gamer'], 50),
                'func': self.save_game
            },
            {
                'label': Text('CONFIGURAÇÕES', FontManager.fonts['Gamer'], 50),
                'func': lambda: GameStateManager.set_state('options')
            },
            {
                'label': Text('MENU PRINCIPAL', FontManager.fonts['Gamer'], 50),
                'func': lambda: GameStateManager.set_state('start')
            },
            {
                'label': Text('SAIR DO JOGO', FontManager.fonts['Gamer'], 50),
                'func': lambda: pygame.quit()
            }
        ]
        self.selected_option = 0  # Opção que está selecionada
        self.option_measures = [500, 105]  # Medidas de cada Opção
        self.display_info = pygame.display.Info()  # Informações sobre a tela

        self.auxiliar_surface = pygame.Surface((
            self.display_info.current_w,
            self.display_info.current_h
        ), pygame.SRCALPHA)

        self.background = pygame.Surface(
            self.auxiliar_surface.get_size(),
            pygame.SRCALPHA
        )
        self.background.fill((0,0,0,200))

        # Informações sobre o cursor que marca qual a opção selecionada
        self.cursor_icon = pygame.transform.scale_by(pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')), 1.5)
        self.cursor_rect = self.cursor_icon.get_rect()

        # Essa variável é responsável por checar se o player entrou na cena com o botão
        # de confirmação selecionado (Enter ou Z), assim eu posso evitar que ele entre
        # na tela ja selecionando a opção por acidente
        self.entered_holding_confirm_button = False

        self.save_response_text = None
        self.save_response_text_maximum_time = FPS*5
        self.save_response_text_time_counter = 0
    
    def save_game(self):
        try:
            SaveManager.save()
        except Exception as e:
            self.save_response_text = Text('NÃO FOI POSSÍVEL SALVAR O JOGO', FontManager.fonts['Gamer'], 70)
        else:
            self.save_response_text = Text('JOGO SALVO COM SUCESSO', FontManager.fonts['Gamer'], 70, (252, 219, 3))
        finally:
            self.save_response_text_time_counter = 0

    def on_first_execution(self):
        pass

    def move_cursor(self, increment):
        if self.selected_option + increment >= len(self.menu_options):
            self.selected_option = 0
        elif self.selected_option + increment < 0:
            self.selected_option = len(self.menu_options)-1
        else:
            self.selected_option += increment

    def run(self):
        # Inicio do ciclo de vida da Cena
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        self.__display.blit(self.auxiliar_surface, self.auxiliar_surface.get_rect())
        self.__display.blit(self.background, self.background.get_rect())

        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.move_cursor(1)  # Movo uma opção pra baixo
                    SoundManager.play_sound('squeak.wav')
                if event.key == pygame.K_UP:
                    self.move_cursor(-1)  # Movo uma opção pra cima
                    SoundManager.play_sound('squeak.wav')
                if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    self.menu_options[self.selected_option]['func']()

        self.cursor_rect.center = (  # Mexo o centro do cursor
            self.menu_options[self.selected_option]['label'].rect.center[0] + 300,  # Matemática para mexer o cursor
            self.menu_options[self.selected_option]['label'].rect.center[1]  # Centralizando o cursor
        )

        if self.save_response_text and self.save_response_text_time_counter <= self.save_response_text_maximum_time:
            self.save_response_text_time_counter += 1
            self.save_response_text.draw(self.__display)

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

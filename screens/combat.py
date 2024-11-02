import pygame
from screens import State
from config import *

from classes.button.button import CombatButton

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

        # Criando o grupo de sprites das opções
        self.buttons_group = pygame.sprite.Group()

        self.cursor = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png'))

        self.options: list[CombatButton] = [
            CombatButton(
                'fight',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
                True
            ),
            CombatButton(
                'act',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
            CombatButton(
                'item',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
            CombatButton(
                'mercy',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
        ]
        self.selected_option = 0
        self.trying_to_move_cursor = False
    

    def move_cursor(self, increment):
        if self.selected_option + increment >= len(self.options):
            self.selected_option = 0
        elif self.selected_option + increment < 0:
            self.selected_option = len(self.options)-1
        else:
            self.selected_option += increment

    
    def on_first_execution(self):
        # Limpando os sons
        self.__sound_manager.stop_music()

    def run(self):
        # Pegando as teclas apertadas
        keys = pygame.key.get_pressed()

        # Preenchendo a tela
        self.__display.fill((0,0,0))

        # Mexendo cursor
        if keys[pygame.K_LEFT] and not self.trying_to_move_cursor:
            self.move_cursor(-1)
            self.trying_to_move_cursor = True
            self.__sound_manager.play_sound('select.wav')
        elif keys[pygame.K_RIGHT] and not self.trying_to_move_cursor:
            self.move_cursor(1)
            self.trying_to_move_cursor = True
            self.__sound_manager.play_sound('select.wav')
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.trying_to_move_cursor = False

        # Ajustando Posição dos botões e suas propriedades
        for i, button in enumerate(self.options):
            if i == self.selected_option:
                button.activated = True
            else:
                button.activated = False

            button.rect.center = (
                (i+1)*(self.__display.get_width()/(len(self.options)+1)),
                self.__display.get_height()-(button.rect.height+40)
            )

        # Desenhando Tudo
        self.buttons_group.draw(self.__display)

        # Dando Update em todos os elementos
        self.buttons_group.update()

        # Fim do ciclo de vida da cena
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
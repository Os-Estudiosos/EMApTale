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
        self.__name = name
        self.__display: pygame.Surface = display
        self.__sound_manager: SoundManager = sound_manager
        self.__game_state_manager: GameStateManager = game_state_manager
        self.__font_manager: FontManager = font_manager

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
        self.selected_option = 0
        self.option_measures = [500, 105]
        self.display_info = pygame.display.Info()

        self.cursor_icon = pygame.transform.scale_by(pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')), 1.5)
        self.cursor_rect = self.cursor_icon.get_rect()

        # Inicializando a Música
        self.__sound_manager.add_music(os.path.join(GET_PROJECT_PATH(), 'sounds', 'the_field_of_dreams.mp3'))
        self.__sound_manager.play_queued_music()

    def move_cursor(self, increment):
        if self.selected_option + increment >= len(self.menu_options):
            self.selected_option = 0
        elif self.selected_option + increment < 0:
            self.selected_option = len(self.menu_options)-1
        else:
            self.selected_option += increment

    def run(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.move_cursor(1)
        elif keys[pygame.K_UP]:
            self.move_cursor(-1)

        self.cursor_rect.center = (
            self.menu_options[self.selected_option]['label'].rect.center[0] + 300,
            self.menu_options[self.selected_option]['label'].rect.center[1]
        )

        for i, option in enumerate(self.menu_options):
            # option['label'].rect.width = self.option_measures[0]
            option['label'].rect.center = (
                self.display_info.current_w/2,
                (self.option_measures[1]/2) + (self.option_measures[1]*(i)) + (self.display_info.current_h-self.option_measures[1]*len(self.menu_options))/2,
            )
            
            # pygame.draw.rect(self.__display, (0, 0, 255), option['label'].rect)
            option['label'].draw(self.__display)
        
        self.__display.blit(self.cursor_icon, self.cursor_rect)


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

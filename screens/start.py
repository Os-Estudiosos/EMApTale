import pygame
import os
from screens import State
from config import GET_PROJECT_PATH
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager


class Start(State):
    def __init__(self, name: str, display: pygame.Surface, sound_manager: SoundManager, game_state_manager: GameStateManager):
        self.__name = name
        self.__display: pygame.Surface = display
        self.__sound_manager: SoundManager = sound_manager
        self.__game_state_manager: GameStateManager = game_state_manager

        self.menu_options = [
            {
                'label': 'INICIAR JOGO'
            },
            {
                'label': 'OPÇÕES'
            },
            {
                'label': 'SAIR',
                'func': lambda: pygame.quit()
            }
        ]
        self.selected_option = 0

        # Inicializando a Música
        self.__sound_manager.add_music(os.path.join(GET_PROJECT_PATH(), 'sounds', 'the_field_of_dreams.mp3'))
        self.__sound_manager.play_queued_music()

    def run(self):
        self.__display.fill((40, 0, 0))

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

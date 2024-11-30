import pygame
import os
from screens import State

from config import *
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.text.text import Text 

class GameoverCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__variables = {}   

        self.random_messages = [ 
            'Lutou bem, tente o IMPA TECH!',
            'Não tankou nem o segundo semestre...',
            'Você falhou e perdeu a borceta'
            'Volte a criar galinhas e capinar mato, amigo!',
            'Perdeu pois nãos arredondaram sua nota de 1,75 para 7',
            'Isso que dar fazer ao mesmo tempo: Junior, Valley, Atlética, Amplia...',
            'Bem que a Bebel avisou sobre as entidades...',
            'ROLAS BEM SUCULENTAS E GROSSAS HAHAHAHAHAHAH'

        ]
        self.__execution_counter = 0

    def on_first_execution(self):
        SoundManager.stop_sound
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "gameover_music.mp3"))

    def run(self):
        # Chama o que será executado apenas na primeira vez
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        self.__display.fill((0, 0, 0))

        # Configura o texto
        text = Text(
            text="GAME", 
            font=FontManager.fonts['Gamer'], 
            size=300, 
            color=(255, 255, 255)
        )
        text2 = Text(
            text="OVER", 
            font=FontManager.fonts['Gamer'], 
            size=300, 
            color=(255, 255, 255)
        )

        # Configura a posição do texto
        text.rect.centerx = self.__display.get_width() // 2
        text.rect.centery = self.__display.get_height() // 2 - 250 

        text2.rect.centerx = self.__display.get_width() // 2
        text2.rect.centery = self.__display.get_height() // 2 - 100  


        # Desenhar o game over
        text.draw(self.__display)
        text2.draw(self.__display)

        pygame.display.flip()

    def on_last_execution(self):    
        self.__execution_counter = 0
        SoundManager.play_music

    @property
    def execution_counter(self):
        return self.execution_counter


    @property
    def display(self):
        return self.display


    @property
    def name(self):
        return self.__name    


    @property
    def game_state_manager(self):
        return self.__game_state_manager

    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value

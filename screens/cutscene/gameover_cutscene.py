import pygame
import os
from screens import State

from config import *
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager
from random import randint

from classes.text.dynamic_text import DynamicText

class GameoverCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__variables = {}

        self.random_messages = [ 
            'Lutou bem, tente o IMPA TECH!',
            'Não tankou nem o segundo semestre...',
            'Volte a criar galinhas e capinar mato, amigo!',
            'Perdeu pois não arredondaram sua nota de 1,75 para 7',
            'Isso que da fazer ao mesmo tempo: Junior, Valley, Atlética, Amplia...',
            'Bem que a Bebel avisou sobre as entidades...',
            'Se fosse GREMISTA teria passado pois o GRÊMIO é IMORTAL tricolor!!!! VAMOS GRÊMIOOOOOOOOOO',
            'O olhar gélido da Luziel entrou na sua alma!'
        ]
        self.__execution_counter = 0

        # Configuração do texto dinâmico
        self.current_text = DynamicText(
            text=self.random_messages[randint(0,len(self.random_messages)-1)],
            font=FontManager.fonts['Pixel'], 
            letters_per_second=8,
            text_size=self.get_resolution_display(),
            max_length=self.__display.get_width() - 70,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
            color=(255, 255, 255),
            sound=None
        )

        self.gameover_image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "gameover.jpg"))


    def get_resolution_display(self):
            """Algo como a responsividade em CSS
            """

            # Pega as dimensões da tela
            info = pygame.display.Info()
            screen_width = info.current_w
            screen_height = info.current_h

            # Verifica a resolução e define valores mutáveis
            if screen_width == 1280 and screen_height == 720:  # HD
                return 30
            elif screen_width == 1920 and screen_height == 1080:  # FHD
                return 40
            else:  
                return 30


    def on_first_execution(self):
        SoundManager.stop_sound
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "gameover_music.mp3"))


    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        # Define as dimensões do que será plotado
        screen_width, screen_height = self.__display.get_size()
        image_width, image_height = self.gameover_image.get_size()

        new_width = screen_width * 0.35
        aspect_ratio = image_height / image_width  
        new_height = new_width * aspect_ratio 

        # Calcular a posição centralizada e levemente para cima
        x_pos = screen_width * 0.5 - new_width * 0.5 
        y_pos = screen_height * 0.5 - new_height * 0.5 - screen_height * 0.2

        resized_image = pygame.transform.scale(self.gameover_image, (int(new_width), int(new_height)))
        image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))

        # Preencher a tela com a imagem de fundo redimensionada
        self.__display.blit(resized_image, image_rect)
        
        # Ajustar o texto para que não ultrapasse a largura da imagem
        text_max_width = new_width  
        self.current_text.max_length = int(text_max_width*1.5) 
        self.current_text.update()

        # Configuração do texto dinâmico
        self.current_text.update()
        self.current_text.draw(self.__display)

        # Pula o game over
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                    self.__game_state_manager.set_state('start')
                    SoundManager.stop_music()

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

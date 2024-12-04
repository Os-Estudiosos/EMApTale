import pygame
import os
from screens import State

from config import *
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.text.dynamic_text import DynamicText

class FinalCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0
        self.__variables = {}

        self.cabra_macho = pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "cabra-macho-ofc.png"))
        self.cabra_macho_text = 'Felicitaciones, apostamos que no lo lograrás, estamos contentos con tu desempeño. ¡Pero estad atentos, porque el próximo semestre el CR aumentará a 9,5! ¡Sigue estudiando!'
        self.black_screen = pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c18.jpeg"))

        self.current_text = DynamicText(
            text=self.cabra_macho_text,
            font=FontManager.fonts['Pixel'], 
            letters_per_second=15,
            text_size=self.get_resolution_display(),
            max_length=self.__display.get_width()/1.9,
            color=(255, 255, 255),
            sound=None
        )

        self.initial_time = 0 # tempo global estático, inicial da cutscenes
        self.current_time_local = 0


    def on_first_execution(self):
        SoundManager.stop_music()
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "finale.mp3"))
        self.initial_time = pygame.time.get_ticks()


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


    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        current_time = pygame.time.get_ticks()
        self.current_time_local = current_time - self.initial_time


        # ============== CONFIG IMAGEM ==============
        # Define as dimensões da tela e da imagem
        screen_width, screen_height = self.__display.get_size()
        image_width, image_height = self.cabra_macho.get_size()

        new_width = screen_width * 0.42  # Aumentado o tamanho do sprite
        aspect_ratio = image_height / image_width
        new_height = new_width * aspect_ratio
        resized_image = pygame.transform.scale(self.cabra_macho, (int(new_width), int(new_height)))

        # Calcula a posição no canto inferior esquerdo
        xi = 0 
        yi = screen_height - new_height  # Inferior

        # Desenha a imagem na tela
        self.__display.blit(resized_image, (xi, yi))


        # ============== CONFIG TEXTO ==============
        # Atualiza o atributo de posição do texto
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        xt = screen_width*0.4
        yt = screen_height*0.4

        self.current_text.position=(xt,yt)

        # Atualiza e desenha o texto dinâmico na tela
        if (255 - self.current_time_local//10) < -7:    
            self.current_text.update()
            self.current_text.draw(self.__display)

        self.black_screen = pygame.transform.scale(self.black_screen, (screen_width, screen_height))
        self.__display.blit(self.black_screen, (0,0))
        self.black_screen.set_alpha(255 - self.current_time_local//10)

        # Pula a cutscene
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                    if (255 - self.current_time_local//10) < -7:
                        if self.current_text.finished:
                            self.__game_state_manager.set_state('start')
                            SoundManager.stop_music()


    def on_last_execution(self):    
        SoundManager.stop_music()


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
    
    
    @property
    def variables(self):
        return self.__variables
    

    @variables.setter
    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value

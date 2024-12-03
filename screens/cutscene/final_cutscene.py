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
        self.cabra_macho_text = 'Parabéns, fez valer a sua bolsa, estamos considerando aumentar o CR mínimo do próximo semestre para 8, então será um pouco mais difícil! Estude e até breve!'
       
        self.current_text = DynamicText(
            text=self.cabra_macho_text,
            font=FontManager.fonts['Pixel'], 
            letters_per_second=15,
            text_size=self.get_resolution_display(),
            max_length=self.__display.get_width() - 70,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
            color=(255, 255, 255),
            sound=None
        )


    def on_first_execution(self):
        SoundManager.stop_music()
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "final.mp3"))


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

        # ============== CONFIG IMAGEM ==============
        # Define as dimensões da tela e da imagem
        screen_width, screen_height = self.__display.get_size()
        image_width, image_height = self.cabra_macho.get_size()

        new_width = screen_width * 0.42  # Aumentado o tamanho do sprite
        aspect_ratio = image_height / image_width
        new_height = new_width * aspect_ratio
        resized_image = pygame.transform.scale(self.cabra_macho, (int(new_width), int(new_height)))

        # Calcula a posição no canto inferior esquerdo
        x_pos = 0 
        y_pos = screen_height - new_height  # Inferior, considerando o tamanho da imagem

        # Desenha a imagem na tela
        self.__display.blit(resized_image, (x_pos, y_pos))


        # ============== CONFIG TEXTO ==============
        image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))

        text_max_width = new_width  
        self.current_text.max_length = int(text_max_width*1) 
        self.current_text.update()

        # Configurações para posicionar o texto no canto superior direito
        top_margin = int(screen_height * 0.3)  
        side_margin = int(screen_width * 0.3)  
        
        # Calcula o comprimento máximo do texto com base na largura disponível
        text_max_width = screen_width - side_margin * 2
        self.current_text.max_length = int(text_max_width)

        # Define a posição do texto no canto superior direito
        x_text = screen_width - side_margin - text_max_width  # Ajusta para alinhar à direita
        y_text = top_margin

        # Atualiza o atributo de posição do texto, caso exista
        self.current_text.position = (x_text, y_text)

        # Atualiza e desenha o texto dinâmico na tela
        self.current_text.update()
        self.current_text.draw(self.__display)


        # Pula a cutscene
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                    self.__game_state_manager.set_state('emap')
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

import pygame
from screens import State
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from classes.text.dynamic_text import DynamicText

class IntroCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        self.stage = 0
        self.texts = [
            "Bem vindo a Fundação Getúlio Vargas nobre guerreiro,",
            "após um semestre de inúmeras batalhas contra diversos inimigos, você se encontra em uma situação difícil... ",
            "Conseguiu, com muito esforço, conquistar um CR de 5.9, mas você quer (e precisa) mais do que isso",
            "buscando a redenção, você pretende encarar as Avaliações Suplementares para se provar digno de um CR 7+",
            "Mas não tenha muito otimisto, pois 5 Entidades Poderosas da EMAP tentarão ardilosamente impedir você de conseguir",
            "Tenha cuidado e nunca se esqueça: você nunca estará sozinho...",
        ]
        self.images = [
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/13.jpg"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/13.jpg"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/13.jpg"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/13.jpg"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/13.jpg"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/14.png"),
        ]
        self.current_text = DynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Game-Font'],
            letters_per_second=10,
            text_size=40,
            max_length=self.__display.get_width() - 40,
            position=(20, self.__display.get_height() // 1.5)
        )
        self.current_image = self.images[self.stage]
        self.music_started = False
        self.wait_after_text = 2000  # Esperar 2 segundos após o texto terminar
        self.last_stage_change_time = 0

    def on_first_execution(self):
        SoundManager.play_music('/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sounds/msc_the_field_of_dreams.mp3')
        self.music_started = True
        self.last_stage_change_time = pygame.time.get_ticks()

    def run(self):
        current_time = pygame.time.get_ticks()

        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        if self.current_text.is_finished and current_time - self.last_stage_change_time > self.wait_after_text:
            self.stage += 1
            if self.stage < len(self.texts):
                self.current_text = DynamicText(
                    text=self.texts[self.stage],
                    font=FontManager.fonts['Game-Font'],
                    letters_per_second=10,
                    text_size=40,
                    max_length=self.__display.get_width() - 40,
                    position=(20, self.__display.get_height() // 1.5)
                )
                self.current_image = self.images[self.stage]
                self.last_stage_change_time = current_time
            else:
                self.show_game_title()
                return

        # Desenho da imagem e texto
        image_rect = self.current_image.get_rect(center=(self.__display.get_width() // 2, self.__display.get_height() // 3))
        self.__display.blit(self.current_image, image_rect)
        self.current_text.update()
        self.current_text.draw(self.__display)

    def show_game_title(self):
        title_text = DynamicText(
            text="EMAPTALE",
            font=FontManager.fonts['Gamer'],
            letters_per_second=15,
            text_size=80,
            position=(self.__display.get_width() // 2 - 150, self.__display.get_height() // 2 - 40)
        )
        title_text.draw(self.__display)
        SoundManager.play_sound('intro_noise.ogg')
        pygame.time.delay(2000)
        self.__game_state_manager.set_state('emap')

    def on_last_execution(self):    
        self.__execution_counter = 0
        self.stage = 0 
        self.current_image = self.images[self.stage]
        self.current_text = self.texts[self.stage]

    
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
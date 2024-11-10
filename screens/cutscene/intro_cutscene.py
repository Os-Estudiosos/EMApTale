import pygame
from screens import State
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from classes.text.cuts_dynamic_text import CDynamicText

class IntroCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        self.stage = 0
        self.texts = [
            "Bem vindo a Fundação Getulio Vargas! Após um longo semestre de inúmeros desafios, você se encontra em uma situação difícil...",
            "Conseguiu, com muito esforço, conquistar um CR 5.9, mas você quer - e precisa - mais do que isso!",
            "Buscando a redenção, você pretende encarar as Avaliações Suplementares para se provar digno de um CR 7+",
            "Mas não tenha otimismo, pois 5 Entidades da EMAp tentarão impedi-lo de conseguir!",
            "       ", 

        ]
        self.images = [
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c11.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c12.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c16.png"), 
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c15.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c17.png"),

        ]
        self.current_text = CDynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Pixel'],
            letters_per_second=17.5,
            text_size=40,
            max_length=self.__display.get_width() - 40,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
            color=(255,255,255)
        )
        self.current_image = self.images[self.stage]


        # Variáveis para controle de tempo, imagem, texto, intervalos, opacidade...
        self.wait_after_text = 100 
        self.last_stage_change_time = 0
        self.initial_time = 0
        self.local_current_time = 0


    def on_first_execution(self):
        # Define uma única vez, o tempo incial da cena
        self.initial_time = pygame.time.get_ticks()

        SoundManager.stop_music()
        SoundManager.play_music("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sounds/intro_history.mp3")
        

    def run(self):

        # Chama o que será executado apenas na primeira vez
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        # Cria um "tempo zero" da cena, vai variar conforme o  
        current_time = pygame.time.get_ticks()
        self.local_current_time = current_time - self.initial_time

        print(current_time, self.local_current_time, self.initial_time, self.local_current_time - self.last_stage_change_time)



        # Marcar o tempo de término do texto apenas uma vez
        if self.current_text.is_finished and self.last_stage_change_time == 0:
            self.last_stage_change_time = current_time


        # Verificar se o tempo de espera passou
        if self.current_text.is_finished and self.local_current_time - self.last_stage_change_time > self.wait_after_text:
            self.stage += 1
            self.last_stage_change_time = 0  # Resetar o tempo
            
            if self.stage < len(self.texts):
                self.current_text = CDynamicText(
                    text=self.texts[self.stage],
                    font=FontManager.fonts['Pixel'],
                    letters_per_second=17.5,
                    text_size=40,
                    max_length=self.__display.get_width() - 40,
                    position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
                    color=(255,255,255)
                )
                self.current_image = self.images[self.stage]



        # Desenho da imagem e texto
        if self.stage < len(self.texts):  
            
            screen_width, screen_height = self.__display.get_size()
            image_width, image_height = self.current_image.get_size()

            # Configura o tamano e a posição da imagem, para a última, deixa em tela cheia
            if  self.stage == len(self.images)-1:
                # Para última imagem, deixa em tela cheia e toca a música
                new_width = screen_width * 1.01
                aspect_ratio = image_height / image_width  
                new_height = new_width * aspect_ratio  
                x_pos = screen_width * 0.5 - new_width * 0.5  
                y_pos = screen_height * 0.5 - new_height * 0.5  
                SoundManager.play_sound("intro_noise.ogg")
                SoundManager.stop_music()

            else:
                # Redimensionar a imagem proporcionalmente
                new_width = screen_width * 0.5  
                aspect_ratio = image_height / image_width  
                new_height = new_width * aspect_ratio  

                # Redimensionar a imagem
                resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))

                # Calcular a posição centralizada e levemente para cima
                x_pos = screen_width * 0.5 - new_width * 0.5 
                y_pos = screen_height * 0.5 - new_height * 0.5 - screen_height * 0.2 


            resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))
            image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))
            # Plota a imagem
            self.__display.blit(resized_image, image_rect)

            # Ajustar o texto para que não ultrapasse a largura da imagem
            text_max_width = new_width  
            self.current_text.max_length = int(text_max_width - 40) 
            self.current_text.update()

            # Plota o texto
            self.current_text.draw(self.__display)    
        
        else:
            self.__game_state_manager.set_state('emap')
            
        
    def on_last_execution(self):    
        self.__execution_counter = 0
        self.stage = 0 
        self.current_image = self.images[self.stage]
        self.current_text = self.texts[self.stage]
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
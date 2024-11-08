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
            "Bem vindo a Fundação Getulio Vargas nobre guerreiro,",
            "após um semestre de inúmeras batalhas contra diversos inimigos, você se encontra em uma situação difícil... ",
            "Conseguiu, com muito esforço, conquistar um CR de 5.9, mas você quer (e precisa) mais do que isso",
            "buscando a redenção, você pretende encarar as Avaliações Suplementares para se provar digno de um CR 7+",
            "Mas não tenha muito otimisto, pois 5 Entidades Poderosas da EMAp tentarão ardilosamente impedir você de conseguir",
            "Tenha cuidado e nunca se esqueça: você nunca estará sozinho...",
            "       ",

        ]
        self.images = [
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c11.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c12.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c13.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c14.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c15.png"), 
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c16.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c17.png"),

        ]
        self.current_text = CDynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Pixel'],
            letters_per_second=13,
            text_size=40,
            max_length=self.__display.get_width() - 40,
            position=(20, self.__display.get_height() // 1.5)
        )
        self.current_image = self.images[self.stage]
        self.wait_after_text = 2000 
        self.last_stage_change_time = 0


    def on_first_execution(self):
        SoundManager.stop_music()
        self.last_stage_change_time = pygame.time.get_ticks()


    def run(self):
        current_time = pygame.time.get_ticks()

        if not self.__execution_counter > 0:
            self.on_first_execution()
            self    .__execution_counter += 1

        # Verificar se o número de textos e imagens está correto
        if len(self.texts) != len(self.images):
            raise TypeError("Quantidade diferente de imagens e textos")

        # Marcar o tempo de término do texto apenas uma vez
        if self.current_text.is_finished and self.last_stage_change_time == 0:
            self.last_stage_change_time = current_time

        # Verificar se o tempo de espera passou
        if self.current_text.is_finished and current_time - self.last_stage_change_time > self.wait_after_text:
            self.stage += 1
            self.last_stage_change_time = 0  # Resetar o tempo

            # Configurar novo texto e imagem apenas se houver mais estágios
            if self.stage < len(self.texts):
                self.current_text = CDynamicText(
                    text=self.texts[self.stage],
                    font=FontManager.fonts['Pixel'],
                    letters_per_second=15,
                    text_size=40,
                    max_length=self.__display.get_width() - 40,
                    position=(20, self.__display.get_height() // 1.5)  # Posição fixa do texto
                )
                self.current_image = self.images[self.stage]

        # Desenho da imagem e texto
        if self.stage < len(self.texts):  # Garante que o estágio seja válido
            # Calcular a posição da imagem no centro, levemente para cima
            screen_width, screen_height = self.__display.get_size()
            image_width, image_height = self.current_image.get_size()

            # Redimensionar a imagem proporcionalmente (exemplo: 30% da largura da tela)
            new_width = screen_width * 0.5  # 30% da largura da tela
            aspect_ratio = image_height / image_width  # Calcula a razão de aspecto original
            new_height = new_width * aspect_ratio  # Ajusta a altura proporcionalmente

            # Redimensionar a imagem
            resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))

            # Calcular a posição centralizada e levemente para cima
            x_pos = screen_width * 0.5 - new_width * 0.5  # Centraliza horizontalmente
            y_pos = screen_height * 0.5 - new_height * 0.5 - screen_height * 0.2  # Centraliza verticalmente e sobe 10%

            image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))
            self.__display.blit(resized_image, image_rect)

            self.current_text.update()
            self.current_text.draw(self.__display)
        else:
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
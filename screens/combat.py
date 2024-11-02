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

        # Carrgando o sprite do cursor
        self.cursor = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png'))

        self.options: list[CombatButton] = [  # Lista com cada botão
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
        self.selected_option = 0  # A opção que eu estou analisando agora
        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido
    

    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        if self.selected_option + increment >= len(self.options):  # Se passar da quantidade de opções
            self.selected_option = 0  # Volto para a primeira
        elif self.selected_option + increment < 0:  # Se for menor que 0
            self.selected_option = len(self.options)-1  # Vou para a última opção
        else:  # Se não
            self.selected_option += increment  # Só ando quantas vezes foi pedido

    
    def on_first_execution(self):
        # Limpando os sons
        self.__sound_manager.stop_music()

    def run(self):
        # Pegando as teclas apertadas
        keys = pygame.key.get_pressed()

        # Preenchendo a tela
        self.__display.fill((0,0,0))

        # Mexendo cursor
        if keys[pygame.K_LEFT] and not self.trying_to_move_cursor:  # Se eu apertar para a esquerda e não tiver nenhuma seta sendo segurada
            self.move_cursor(-1)  # Movo uma opção
            self.trying_to_move_cursor = True  # Estou tentando mexer o cursor
            self.__sound_manager.play_sound('select.wav')  # Toco o som de trocar opção
        elif keys[pygame.K_RIGHT] and not self.trying_to_move_cursor:  # Se eu aprtar para a direita e não tiver nenhuma seta sendo segurada
            self.move_cursor(1)
            self.trying_to_move_cursor = True
            self.__sound_manager.play_sound('select.wav')
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            # Só permito mexer de novo o cursor se eu soltar a tecla e apertar de novo
            self.trying_to_move_cursor = False

        # Ajustando Posição dos botões e suas propriedades
        for i, button in enumerate(self.options):
            if i == self.selected_option:  # Se o botão que eu estiver analisando for a opção selecionada
                button.activated = True  # Eu marco a propriedade de ativado
            else:
                button.activated = False  # Eu removo a propriedade de ativado

            button.rect.center = (  # Centralizo o botão
                (i+1)*(self.__display.get_width()/(len(self.options)+1)),  # Matemática para centralizar os botão bonitinho
                self.__display.get_height()-(button.rect.height+40)  # Mais matemática pra posicionamento
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
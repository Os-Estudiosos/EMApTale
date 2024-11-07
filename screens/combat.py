import pygame
from screens import State

from config import *

from classes.battle.button import CombatButton
from classes.battle.container import BattleContainer
from classes.battle.hp_container import HPContainer
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.battle.menus.main_menu import MainMenu
from classes.battle.menus.inventory_menu import InventoryMenu

from classes.text.dynamic_text import DynamicText
from classes.text.text import Text

from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager

from classes.battle.heart import Heart


class Combat(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        game_state_manager: GameStateManager,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display
        self.__game_state_manager: GameStateManager = game_state_manager

        self.__execution_counter = 0

        # Criando os groups de sprites
        self.text_groups = pygame.sprite.Group()  # Grupo dos textos
        self.player_group = pygame.sprite.Group()  # Grupo do player

        # ============ VARIÁVEIS DO HUD ============
        # Carregando o background da batalha
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'battle-background.png')),
            (self.__display.get_width()/1.2, 300)
        )
        self.background_rect = self.background.get_rect()
        self.background_rect.centerx = self.__display.get_width()/2
        self.background_rect.y = 10

        # Iniciando o container da Batalha
        self.battle_container = BattleContainer(self.__display)

        # Variáveis do Jogador
        self.player = Heart(self.battle_container, self.player_group)

        # Variável que gerencia o turno
        self.turn = 'player'  # "player" ou "boss"

        # Variáveis relacionadas ao menu que do turno do player
        # self.battle_menu_manager = BattleMenuManager()

        # Definindo todos os menus
        self.inventory_menu = InventoryMenu(self.battle_container)
        self.main_menu = MainMenu(self.__display)

        BattleMenuManager.menus = {
            f'{self.inventory_menu.__class__.__name__}': self.inventory_menu
        }

    def on_first_execution(self):
        # Limpando os sons
        SoundManager.stop_music()

    def run(self):
        # Inicio do ciclo de vida da cena
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
        
        # Ajustando o nome do personagem
        text_player_name = Text(self.player.name.upper(), FontManager.fonts['Gamer'], 60)
        text_player_name.rect.x = self.main_menu.options[0].rect.x
        text_player_name.rect.y = self.main_menu.options[0].rect.y - 1.5*text_player_name.rect.height

        # Ajustando o HP do personagem (Na tela)
        hp_container = HPContainer(self.player)
        hp_container.inner_rect.center = [
            self.__display.get_width()/2,
            text_player_name.rect.centery
        ]

        # ============ DESENHANDO O BACKGROUND ============
        self.__display.blit(self.background, self.background_rect)

        # ============ DANDO UPDATE NOS ELEMENTOS GERAIS ============
        self.battle_container.update()
        hp_container.update()
        self.battle_container.update()
        self.main_menu.update()

        # ============ DESENHANDO TUDO ============
        self.battle_container.draw()
        text_player_name.draw(self.__display)
        hp_container.draw(self.__display)
        self.main_menu.draw()

        # ============ FAZENDO ISSO TUDO COM O MENU ============
        if BattleMenuManager.active_menu:
            BattleMenuManager.active_menu.draw()
            BattleMenuManager.active_menu.update()

        for btn in self.main_menu.options:
            btn.draw_cursor(self.__display)

        # Ajustando o container da batalha para ficar em cima da vida do jogador
        self.battle_container.out_rect.bottom = hp_container.inner_rect.bottom - 50

        # Pegando as teclas apertadas
        keys = pygame.key.get_pressed()

        # ============ CÓDIGO RELACIONADO AOS TURNOS ============
        # Se for o turno do Player
        if self.turn == 'player':
            # ============ HUD QUE SÓ APARECE NO TURNO DO PLAYER ============
            # Esse monte de self.option é para deixar numa largura onde o lado esquerdo fica alinhado com o primeiro botão e o direito com o útlimo botão
            self.battle_container.resize(
                self.main_menu.options[len(self.main_menu.options)-1].rect.right - self.main_menu.options[0].rect.left,
                self.__display.get_height()/2-30
            )  # Redesenho o container da batalha

            # Ajustando os botões do HUD
            for i, button in enumerate(self.main_menu.options):
                if i == self.main_menu.selected_option:  # Se o botão que eu estiver analisando for a opção selecionada
                    button.activated = True  # Eu marco a propriedade de ativado
                else:
                    button.activated = False  # Eu removo a propriedade de ativado
                    
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                # Só permito mexer de novo o cursor se eu soltar a tecla e apertar de novo
                self.trying_to_move_cursor = False

            # ========== ATUALIZANDO AS COISAS QUE SÓ APARECEM NO TURNO DO PLAYER ==========

            # ========== DESENHANDO AS COISAS QUE SÓ APARECEM NO TURNO DO PLAYER ==========

        else:  # Se não for o turno do player
            self.battle_container.resize(self.__display.get_width()/3, self.__display.get_height()/2-30)  # Redimensiono o container da batalha

            for btn in self.battle_container.options:  # Ajustando para nenhum botão ficar selecionado
                btn.activated = False
            
            if keys[pygame.K_u]:
                self.player.apply_effect('inverse')
            
            # Draws que são apenas no turno do boss
            self.player_group.draw(self.__display)
            
            # Updates que são apenas do turno do boss
            self.player_group.update(display=self.__display)
    
    def on_last_execution(self):
        self.__execution_counter = 0

    @property
    def execution_counter(self):
        return self.execution_counter

    @property
    def display(self):
        return self.display
    
    @property
    def game_state_manager(self):
        return self.__game_state_manager
    
    @property
    def name(self):
        return self.__name

    @property
    def variables(self):
        return self.__variables
    
    @variables.setter
    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value
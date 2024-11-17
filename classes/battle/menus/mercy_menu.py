import pygame
import os
import math

from config import *
from config.fontmanager import FontManager
from config.soundmanager import SoundManager

from classes.battle.container import BattleContainer
from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.text.dynamic_text import DynamicText

class MercyMenu(BattleMenu):
    def __init__(self, battle_container: BattleContainer):
        self.__options: list[dict] = []  # Lista de opções
        self.container = battle_container  # Container dos menus
        self.display = pygame.display.get_surface()  # A tela do jogo

        self.selected_option = 0
        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido

        # Carregando o sprite do cursor
        self.cursor = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
            1.8
        )
        self.cursor_rect = self.cursor.get_rect()

        self.runtime_counter = 0  # Previnir que entre clicando nos itens
        self.entered_pressing = False

        self.text_to_show = DynamicText(
            'Piedade não é uma opção',
            FontManager.fonts['Gamer'],
            10,
            int((450*100)/self.display.get_height()),
            self.container.inner_rect.width,
            sound='text_2.wav'
        )
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        self.selected_option = (self.selected_option+increment)%len(self.__options)

        self.page = math.floor(self.selected_option/(self.items_per_page))
    
    def on_first_execution(self):
        keys = pygame.key.get_pressed()
        self.runtime_counter += 1
        if keys[pygame.K_z] or keys[pygame.K_RETURN]:
            self.entered_pressing = True

    def update(self):
        if self.runtime_counter == 0:
            self.on_first_execution()

        keys = pygame.key.get_pressed()  # Pegando o dicinoário das teclas

        # ====== CÓDIGO AQUI ======
        self.text_to_show.position = (
            self.container.inner_rect.x+10,
            self.container.inner_rect.y+10
        )
        self.text_to_show.update()

        # Volto no menu anterior
        if keys[pygame.K_x] or keys[pygame.K_BACKSPACE]:  # Para eu voltar no menu anterior
            BattleMenuManager.go_back()
    
    def draw(self):
        self.text_to_show.draw(self.display)
    
    @property
    def options(self):
        return self.__options

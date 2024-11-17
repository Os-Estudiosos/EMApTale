import pygame
import os
import math

from config import *
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.combatmanager import CombatManager
from config.eventmanager import EventManager

from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.battle.menus.hud.damage_bar import DamageBar
from classes.battle.menus.hud.cut import Cut

class FightMenu(BattleMenu):
    def __init__(self):
        self.__options: list[dict] = []  # Lista de opções
        self.container = CombatManager.get_variable('battle_container')  # Container dos menus
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

        self.damage_indicator = pygame.transform.scale(  # Imagem de fundo do menu
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_indicator.png')),
            self.container.inner_rect.size
        )
        self.damage_indicator_rect = self.damage_indicator.get_rect()

        self.damage_bar = DamageBar()  # Barrinha que indica onde temos que atacar
        self.cut = Cut()  # O Corte que aparece na animação

        self.attacked = False  # Variável que diz se eu vou mostrar o corte na tela ou não
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        self.selected_option = (self.selected_option+increment)%len(self.__options)

        self.page = math.floor(self.selected_option/(self.items_per_page))
    
    def on_first_execution(self):
        """Função que executa na primeira vez que o menu aparece
        """
        self.runtime_counter += 1  # Aumento o contador de vezes que rodou
        self.damage_bar.choose_direction()  # Escolho de onde o indicador de dano vai vir
        self.attacked = False
        EventManager.clear()

    def update(self):
        if self.runtime_counter == 0:  # Executo a primeira vez
            self.on_first_execution()

        # Fico escalonando o indicador do dano
        self.damage_indicator = pygame.transform.scale(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_indicator.png')),
            self.container.inner_rect.size
        )
        self.damage_indicator_rect = self.damage_indicator.get_rect()

        # Centralizo o indicador de dano
        self.damage_indicator_rect.x = self.container.inner_rect.x
        self.damage_indicator_rect.y = self.container.inner_rect.y

        self.damage_bar.update()

        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and not self.attacked:
                    self.cut.animate()
                    self.attacked = True
                    SoundManager.play_sound('attack_sound.wav')

        if self.attacked:
            self.cut.update()

    
    def draw(self):
        self.display.blit(self.damage_indicator, self.damage_indicator_rect)
        self.display.blit(self.damage_bar.image, self.damage_bar.rect)
        if self.attacked and self.cut.animating:
            self.display.blit(self.cut.image, self.cut.rect)
    
    @property
    def options(self):
        return self.__options

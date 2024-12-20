import pygame
import os

from config import *
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager
from classes.battle.button import CombatButton

from classes.player import Player

class MainMenu(BattleMenu):
    def __init__(self, screen: pygame.Surface):
        self.__display = screen

        # Carregando o sprite do cursor
        self.cursor = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
            1.8
        )
        self.cursor_rect = self.cursor.get_rect()

        self.buttons_group = pygame.sprite.Group()  # Grupo dos botões

        self.__options: list[CombatButton] = [  # Lista com cada botão
            CombatButton(
                'fight',
                lambda: BattleMenuManager.change_active_menu('FightMenu'),
                self.__display,
                [ self.buttons_group ],
                True
            ),
            CombatButton(
                'act',
                lambda: BattleMenuManager.change_active_menu('ActMenu'),
                self.__display,
                [ self.buttons_group ],
            ),
            CombatButton(
                'item',
                lambda: BattleMenuManager.change_active_menu('InventoryMenu'),
                self.__display,
                [ self.buttons_group ],
            ),
            CombatButton(
                'mercy',
                lambda: BattleMenuManager.change_active_menu('MercyMenu'),
                self.__display,
                [ self.buttons_group ],
            ),
        ]
        self.selected_option = 0  # A opção que eu estou analisando agora

        self.adjust_buttons_position()
    
    def adjust_buttons_position(self):
        # Ajustando Posição dos botões e suas propriedades
        for i, button in enumerate(self.__options):
            button.rect.center = (  # Centralizo o botão
                (i+1)*(self.__display.get_width()/(len(self.__options)+1)),
                # Matemática para centralizar os botão bonitinho
                self.__display.get_height()-(button.rect.height)
                # Mais matemática pra posicionamento
            )
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        if self.selected_option + increment >= len(self.__options):  # Se passar da quantidade de opções
            self.selected_option = 0  # Volto para a primeira
        elif self.selected_option + increment < 0:  # Se for menor que 0
            self.selected_option = len(self.__options)-1  # Vou para a última opção
        else:  # Se não
            self.selected_option += increment  # Só ando quantas vezes foi pedido

    def update(self):
        # Alterar lugar onde o cursor está sendo desenhado posterioremente
        self.cursor_rect.center = (
            self.__options[self.selected_option].rect.centerx - 70,
            self.__options[self.selected_option].rect.centery
        )

        # ============ CÓDIGO RELACIONADO AO CURSOR ============
        if BattleMenuManager.active_menu  == self.__class__.__name__:
            # Mexendo o cursor
            for event in EventManager.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_cursor(-1)  # Movo uma opção
                        SoundManager.play_sound('squeak.wav')  # Toco o som de trocar opção
                    elif event.key == pygame.K_RIGHT:
                        self.move_cursor(1)
                        SoundManager.play_sound('squeak.wav')
                    elif event.key == pygame.K_z or event.key == pygame.K_RETURN:
                        self.__options[self.selected_option].on_click()
                        SoundManager.play_sound('select.wav')
    
    def draw(self):
        self.buttons_group.draw(self.__display)

        if BattleMenuManager.active_menu  == self.__class__.__name__:
            self.display.blit(self.cursor, self.cursor_rect)

    @property
    def options(self):
        return self.__options
    
    @property
    def display(self):
        return self.__display

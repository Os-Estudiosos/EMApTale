import pygame
import os

from config import *
from config.soundmanager import SoundManager

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

        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido

        self.__options: list[CombatButton] = [  # Lista com cada botão
            CombatButton(
                'fight',
                lambda: print('Lutar'),
                self.__display,
                [ self.buttons_group ],
                True
            ),
            CombatButton(
                'act',
                lambda: print('Agir'),
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
                lambda: print('Piedade'),
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
        keys = pygame.key.get_pressed()

        # Alterar lugar onde o cursor está sendo desenhado posterioremente
        self.cursor_rect.center = (
            self.__options[self.selected_option].rect.centerx - 70,
            self.__options[self.selected_option].rect.centery
        )

        # ============ CÓDIGO RELACIONADO AO CURSOR ============
        if BattleMenuManager.active_menu  == self.__class__.__name__:
            # Mexendo cursor
            if keys[pygame.K_LEFT] and not self.trying_to_move_cursor:  # Se eu apertar para a esquerda e não tiver nenhuma seta sendo segurada
                self.move_cursor(-1)  # Movo uma opção
                self.trying_to_move_cursor = True  # Estou tentando mexer o cursor
                SoundManager.play_sound('select.wav')  # Toco o som de trocar opção
            elif keys[pygame.K_RIGHT] and not self.trying_to_move_cursor:  # Se eu aprtar para a direita e não tiver nenhuma seta sendo segurada
                self.move_cursor(1)
                self.trying_to_move_cursor = True
                SoundManager.play_sound('select.wav')
            
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.trying_to_move_cursor = False
            
            if keys[pygame.K_z] or keys[pygame.K_RETURN]:
                self.__options[self.selected_option].on_click()
    
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
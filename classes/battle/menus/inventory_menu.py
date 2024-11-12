import pygame
import os
import math

from config import *
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.battle.container import BattleContainer
from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.player import Player
from classes.text.text import Text
from classes.text.dynamic_text import DynamicText

from utils import sign

class InventoryMenu(BattleMenu):
    def __init__(self, battle_container: BattleContainer):
        self.__options: list[dict] = []  # Lista de opções
        self.container = battle_container  # Container dos menus
        self.display = pygame.display.get_surface()  # A tela do jogo

        self.selected_option = 0
        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido

        # Carregando o sprite do cursor
        self.cursor = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
            1.5
        )
        self.cursor_rect = self.cursor.get_rect()

        # Adicionando os itens como minhas opções
        for i, item in enumerate(Player.inventory):
            if item.type == 'miscellaneous':
                self.__options.append({
                    'text': Text(f'* {item.name}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                    'func': item.func
                })
        
        self.page = 0
        self.items_per_column = 100
        for i, opt in enumerate(self.__options):
            if opt['text'].rect.height*i > self.container.inner_rect.height:
                self.items_per_column = i
                break
        
        self.items_per_page = self.items_per_column * 2

        self.runtime_counter = 0  # Previnir que entre clicando nos itens

        self.no_items_text = DynamicText(
            'Você não tem itens no inventário',
            FontManager.fonts['Gamer'],
            20,
            int((450*100)/self.display.get_height()),
            self.container.inner_rect.width,
            (0,0),
            sound='text.wav'
        )
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        self.selected_option = (self.selected_option+increment)%len(self.__options)

        self.page = math.floor(self.selected_option/(self.items_per_page))
    
    def on_first_execution(self):
        self.runtime_counter += 1
        self.no_items_text.restart()  # Reinicio o texto de não ter item no inventário
        EventManager.clear()

    def update(self):
        if self.runtime_counter == 0:
            self.on_first_execution()

        if len(self.__options) > 0:  # Se eu tiver itens no inventário
            # Ajusto o cursor
            self.cursor_rect.center = self.__options[self.selected_option%len(self.__options)]['text'].rect.center
            self.cursor_rect.right = self.__options[self.selected_option%len(self.__options)]['text'].rect.left

            # Movendo o cursor pelos itens do inventário
            for event in EventManager.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.move_cursor(1)
                        SoundManager.play_sound('select.wav')
                    elif event.key == pygame.K_UP:
                        self.move_cursor(-1)
                        SoundManager.play_sound('select.wav')
                    elif event.key == pygame.K_LEFT:
                        self.move_cursor(-self.items_per_column)
                        SoundManager.play_sound('select.wav')
                    elif event.key == pygame.K_RIGHT:
                        self.move_cursor(self.items_per_column)
                        SoundManager.play_sound('select.wav')   
                         
                    # Selecionando um item
                    if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and 0 <= self.selected_option < len(self.__options):
                        self.__options[self.selected_option]['func']()
                        self.__options.pop(self.selected_option)
                        Player.inventory.remove_item(self.selected_option)
                        self.entered_pressing = True
        else: # Se não tiver itens
            # Mostro na tela o texto de inventário vazio
            self.no_items_text.update()
            self.no_items_text.position = (
                self.container.inner_rect.x+10,
                self.container.inner_rect.y+10,
            )
        
        # Volto no menu anterior
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] or keys[pygame.K_BACKSPACE]:  # Para eu voltar no menu anterior
            BattleMenuManager.go_back()
    
    def draw(self):
        column = 0
        for i in range(self.items_per_page):
            if i >= self.items_per_column:
                column = 1
            
            if (i+self.items_per_page*self.page) >= len(self.__options):
                break
            
            self.__options[(i+self.items_per_page*self.page)]['text'].rect.x = self.container.inner_rect.x + 10*abs(column-1) + self.container.inner_rect.width*column/2 + (1 - 2 * column)*self.cursor_rect.width
            self.__options[(i+self.items_per_page*self.page)]['text'].rect.y = self.container.inner_rect.y + self.__options[(i+self.items_per_page*self.page)]['text'].rect.height*(i%self.items_per_column)

            self.__options[(i+self.items_per_page*self.page)]['text'].draw(self.display)
        
        if len(self.__options) > 0:
            self.display.blit(self.cursor, self.cursor_rect)
        else:
            self.no_items_text.draw(self.display)
    
    @property
    def options(self):
        return self.__options

import pygame
import os

from config import *
from config.globalmanager import GlobalManager
from config.fontmanager import FontManager
from config.eventmanager import EventManager
from config.soundmanager import SoundManager

from classes.text.text import Text

from classes.player import Player


class InfosHud:
    def __init__(self):
        chatbox_sprite = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'chatbox.png'))

        self.display = pygame.display.get_surface()   # Pego a superfície da tela

        self.stats_sprite_scale_dict = {
            'width': 4.71,
            'height': 4.59,
            'x': 17.74,
            'y': 9.97
        }
        self.stats_sprite = pygame.transform.scale(  # Container com as informações atuais do player
            chatbox_sprite,
            (
                self.display.get_width()/self.stats_sprite_scale_dict['width'],
                self.display.get_height()/self.stats_sprite_scale_dict['height']
            )
        )
        self.stats_rect = self.stats_sprite.get_rect()
        self.stats_rect.y = self.display.get_height()/self.stats_sprite_scale_dict['y']
        self.stats_rect.x = self.display.get_width()/self.stats_sprite_scale_dict['x']

        # Informações que serão mostradas no status
        self.status_texts = [
            Text(Player.name, FontManager.fonts['Gamer'], 50),
            Text(f'HP {Player.life}/{Player.max_life}', FontManager.fonts['Gamer'], 30),
            Text(f'LV {Player.level}', FontManager.fonts['Gamer'], 30)
        ]

        for i, status in enumerate(self.status_texts):
            status.rect.x = self.stats_rect.x+30
            status.rect.y = self.stats_rect.y+(i)*(status.rect.height) + 20
            if i > 0:
                status.rect.y += 20

        # DEFININDO O CONTEINER DAS OPÇÕES E AS OPÇÕES
        self.options_sprite_scale_dict = {  # Dicionário com as medidas de escala para divisão
            'width': 4.71,
            'height': 4.26,
            'x': 17.74,
            'y': 2.86
        }
        self.options_sprite = pygame.transform.scale(  # Container com as opções disponíveis
            chatbox_sprite,
            (
                self.display.get_width()/self.options_sprite_scale_dict['width'],
                self.display.get_height()/self.options_sprite_scale_dict['height']
            )
        )
        self.options_rect = self.options_sprite.get_rect()
        self.options_rect.y = self.display.get_height()/self.options_sprite_scale_dict['y']
        self.options_rect.x = self.display.get_width()/self.options_sprite_scale_dict['x']

        self.option_selected = None  # Qual opção está selecionada para visualizar
        self.options = [  # Lista das opções
            {
                'label': Text('INVENTÁRIO', FontManager.fonts['Gamer'], 50),
                'value': 'inventory'
            },
            {
                'label': Text('STATUS', FontManager.fonts['Gamer'], 50),
                'value': 'status'
            }
        ]

        for i, option in enumerate(self.options):
            option['label'].rect.x = self.options_rect.x+30
            option['label'].rect.y = self.options_rect.y+(i)*(option['label'].rect.height)+20

        # Informações sobre o cursor que marca qual a opção selecionada
        self.cursor_icon = pygame.transform.scale_by(pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')), 1.5)
        self.cursor_rect = self.cursor_icon.get_rect()
        self.wich_one_cursor_is_on = 0  # Qual opção o cursor está selecionando

        self.result_sprite_scale_dict = {
            'width': 2.48,
            'height': 1.25,
            'x': 3.48,
            'y': 9.97
        }
        self.result_sprite = pygame.transform.scale(  # O container que tem as informações da opção escolhida
            chatbox_sprite,
            (
                self.display.get_width()/self.result_sprite_scale_dict['width'],
                self.display.get_height()/self.result_sprite_scale_dict['height']
            )
        )
        self.result_rect = self.result_sprite.get_rect()
        self.result_rect.y = self.display.get_height()/self.result_sprite_scale_dict['y']
        self.result_rect.x = self.display.get_width()/self.result_sprite_scale_dict['x']

        # Informações para o inventário
        self.items_per_page = 10
        self.items_per_column = 5
        self.page = 0
    
    def move_cursor(self, increment):
        self.wich_one_cursor_is_on = (self.wich_one_cursor_is_on+increment)%len(self.options)

    def update(self):
        # Atualizando a posição do cursor
        self.cursor_rect.left = self.options[self.wich_one_cursor_is_on]['label'].rect.right
        self.cursor_rect.centery = self.options[self.wich_one_cursor_is_on]['label'].rect.centery

        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.move_cursor(1)  # Movo uma opção pra baixo
                    SoundManager.play_sound('squeak.wav')
                if event.key == pygame.K_UP:
                    self.move_cursor(-1)  # Movo uma opção pra cima
                    SoundManager.play_sound('squeak.wav')
                if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    self.option_selected = self.options[self.wich_one_cursor_is_on]['value']
                if event.key == pygame.K_x or event.key == pygame.K_BACKSPACE:
                    if self.option_selected:
                        self.option_selected = None
                    else:
                        GlobalManager.on_inventory = False

    def draw(self):
        self.display.blit(self.stats_sprite, self.stats_rect)
        self.display.blit(self.options_sprite, self.options_rect)

        self.display.blit(self.cursor_icon, self.cursor_rect)

        for status in self.status_texts:
            status.draw(self.display)

        if self.option_selected:
            self.display.blit(self.result_sprite, self.result_rect)

        column = 0
        if self.option_selected == 'inventory':  # Se eu selecionar inventário
            for i in range(self.items_per_page):
                if i >= self.items_per_column:
                    column = 1
                
                if (i+self.items_per_page*self.page) >= len(Player.inventory):
                    break
                    
                item = Player.inventory[(i+self.items_per_page*self.page)]
                item_text = Text(f'{item.name}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height()))

                item_text.rect.x = self.result_rect.x + 10*abs(column-1) + self.result_rect.width*column/2 + (1 - 2 * column)*self.cursor_rect.width
                item_text.rect.y = self.result_rect.y + item_text.rect.height*(i%self.items_per_column) + 30

                item_text.draw(self.display)
        
        for i, option in enumerate(self.options):
            option['label'].draw(self.display)

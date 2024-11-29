import pygame
import os
import math

from config import *
from config.globalmanager import GlobalManager
from config.fontmanager import FontManager
from config.eventmanager import EventManager
from config.soundmanager import SoundManager

from classes.text.text import Text
from classes.text.dynamic_text import DynamicText

from classes.player import Player


class InfosHud:
    def __init__(self, items_group):
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

        ########### Informações para o inventário
        self.inventory_items = [
            {
                'text': Text(f'{item.name}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'item': item
            } for item in Player.inventory
        ]

        self.items_per_column = math.floor(self.result_rect.height // self.inventory_items[0]['text'].rect.height)-3
        self.items_per_page = self.items_per_column
        self.page = 0
        self.selected_item = 0
        self.item_is_selected = False  # Quando eu aperto enter e seleciono um item

        ### Informações das ações que podem fazer num item
        self.inventory_actions = [
            {
                'text': Text(f'USAR', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'action': self.use_item
            },
            {
                'text': Text(f'INFO', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'action': self.show_item_description
            },
            {
                'text': Text(f'LARGAR', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'action': self.drop_item
            }
        ]

        self.items_group: pygame.sprite.Group = items_group

        self.show_item_description_text = False
        self.wich_inventory_action = 0
        self.item_description_text = DynamicText(
            '',
            FontManager.fonts['Gamer'],
            20,
            int((450*100)/self.display.get_height()),
            self.result_rect.width - 60,
            (
                self.result_rect.x + 30,
                self.result_rect.y + 30
            ),
            sound='text_1.wav'
        )
        
    def move_cursor(self, increment: int):
        """Função responsável por mover os cursores pelas telas do menu

        Args:
            increment (int): Quanto vai aumentar
        """
        if self.option_selected == 'inventory':
            if not self.item_is_selected:
                self.selected_item = (self.selected_item+increment)%len(self.inventory_items)
                self.page = math.floor(self.selected_item/(self.items_per_page))
            else:
                self.wich_inventory_action = (self.wich_inventory_action+increment)%len(self.inventory_actions)
        if not self.option_selected:
            self.wich_one_cursor_is_on = (self.wich_one_cursor_is_on+increment)%len(self.options)

    def show_item_description(self):
        """Função que faz com que eu mostre a descrição do item selecionado
        """
        self.show_item_description_text = True
        self.item_description_text.restart(Player.inventory[self.selected_item].description)
    
    def update_infos(self):
        self.status_texts = [
            Text(Player.name, FontManager.fonts['Gamer'], 50),
            Text(f'HP {Player.life}/{Player.max_life}', FontManager.fonts['Gamer'], 30),
            Text(f'LV {Player.level}', FontManager.fonts['Gamer'], 30)
        ]
        self.inventory_items = [
            {
                'text': Text(f'{item.name}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'item': item
            } for item in Player.inventory
        ]
        for i, status in enumerate(self.status_texts):
            status.rect.x = self.stats_rect.x+30
            status.rect.y = self.stats_rect.y+(i)*(status.rect.height) + 20
            if i > 0:
                status.rect.y += 20


    def use_item(self):
        """Função que utiliza o item selecionado
        """
        item = self.inventory_items[self.selected_item]['item']
        if item.type == 'miscellaneous':
            item.func()
            Player.inventory.remove_item(item.id)
            self.update_infos()
            self.item_is_selected = False
            self.selected_item = 0
    
    def drop_item(self):
        """Função que larga um item no chão
        """
        item = self.inventory_items[self.selected_item]['item']
        if not item.equiped:
            item.original_rect.centerx = Player.map_position[0]
            item.original_rect.centery = Player.map_position[1]
            self.items_group.add(item)
            GlobalManager.camera.add(item)
            self.item_is_selected = False
            self.selected_item = 0
            Player.inventory.remove_item(item.id)

    def update(self):
        """Função que roda todo quadro
        """
        # Atualizando a posição do cursor
        if not self.option_selected:
            self.cursor_rect.left = self.options[self.wich_one_cursor_is_on]['label'].rect.right
            self.cursor_rect.centery = self.options[self.wich_one_cursor_is_on]['label'].rect.centery
        
        if self.show_item_description_text:
            self.item_description_text.update()

        if self.option_selected == 'inventory':
            # Atualizando a posição do texto que indica as ações que pode fazer com um item
            for i in range(len(self.inventory_actions)):
                opt = self.inventory_actions[i]['text']
                opt.rect.x = self.result_rect.width//(len(self.inventory_actions)+1)*i + self.result_rect.x + 30
                opt.rect.bottom = self.result_rect.bottom - 30
            
            if not self.item_is_selected:
                self.cursor_rect.right = self.inventory_items[self.selected_item]['text'].rect.left
                self.cursor_rect.centery = self.inventory_items[self.selected_item]['text'].rect.centery

            if self.item_is_selected:
                self.cursor_rect.left = self.inventory_actions[self.wich_inventory_action]['text'].rect.right
                self.cursor_rect.centery = self.inventory_actions[self.wich_inventory_action]['text'].rect.centery

        for event in EventManager.events:  # Analiso todos os eventos
            if event.type == pygame.KEYDOWN:  # Se o evento for tecla apertada
                if self.item_is_selected:  # Se eu estiver lidando com um item que selecionei
                    ################## Posso ir para a esquerda ou direita nas opções
                    if event.key == pygame.K_LEFT and self.item_is_selected:
                        self.move_cursor(-1)
                        SoundManager.play_sound('squeak.wav')
                    if event.key == pygame.K_RIGHT and self.item_is_selected:
                        self.move_cursor(1)
                        SoundManager.play_sound('squeak.wav')
                    ##################
                    ################## Se eu selecionar o item
                    if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                        if self.show_item_description_text:
                            self.show_item_description_text = False
                        else:
                            self.inventory_actions[self.wich_inventory_action]['action']()
                    ##################
                    ################## Se eu cancelar a seleção
                    if event.key == pygame.K_x or event.key == pygame.K_BACKSPACE:
                        self.item_is_selected = False
                    ##################
                else:  ################## Se não for um item
                    ##################  Movo a opção pra baixo
                    if event.key == pygame.K_DOWN:
                        self.move_cursor(1)  # Movo uma opção pra baixo
                        SoundManager.play_sound('squeak.wav')
                    ##################  Movo para cima
                    if event.key == pygame.K_UP:
                        self.move_cursor(-1)  # Movo uma opção pra cima
                        SoundManager.play_sound('squeak.wav')
                    ##################  Seleciono a opção
                    if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                        ## Se eu estiver no inventário
                        if self.option_selected == 'inventory':
                            self.item_is_selected = True  # Eu selecionei um item
                            SoundManager.play_sound('item.wav')

                        ## Se eu estiver nas opções iniciais
                        if not self.option_selected:
                            ## Eu indico se eu selecionei o inventário ou os status
                            self.option_selected = self.options[self.wich_one_cursor_is_on]['value']
                            SoundManager.play_sound('select.wav')
                    ## Se eu aperei para cancelar alguma seleção
                    if event.key == pygame.K_x or event.key == pygame.K_BACKSPACE:
                        if self.option_selected:  # Se eu tiver selecionado qualquer opção
                            self.option_selected = None  # Eu a cancelo
                        else:  # Do contrário
                            GlobalManager.on_inventory = False  # Eu saio do inventário (Menu de HUD)

    def draw(self):
        """Função que desenha todas as informações e telas do HUD
        """
        self.display.blit(self.stats_sprite, self.stats_rect)
        self.display.blit(self.options_sprite, self.options_rect)

        for status in self.status_texts:
            status.draw(self.display)

        if self.option_selected:
            self.display.blit(self.result_sprite, self.result_rect)

        column = 0
        if not self.show_item_description_text:
            if self.option_selected == 'inventory':  # Se eu selecionar inventário
                # Desenhando os itens que estão no inventário
                for i in range(self.items_per_page):
                    if (i+self.items_per_page*self.page) >= len(Player.inventory):
                        break
                    
                    item_text = self.inventory_items[(i+self.items_per_page*self.page)]['text']

                    item_text.rect.x = self.result_rect.x + 10*abs(column-1) + self.result_rect.width*column/2 + (1 - 2 * column)*self.cursor_rect.width
                    item_text.rect.y = self.result_rect.y + item_text.rect.height*(i%self.items_per_column) + 30

                    item_text.draw(self.display)
                
                # Desenhando as opções do que pode fazer com os itens
                for opt in self.inventory_actions:
                    opt['text'].draw(self.display)
        else:
            self.item_description_text.draw(self.display)

        for i, option in enumerate(self.options):
                option['label'].draw(self.display)

        if not self.show_item_description_text:
            self.display.blit(self.cursor_icon, self.cursor_rect)

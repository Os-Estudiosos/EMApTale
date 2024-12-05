import pygame
import os
import math

from constants import BOSS_TURN_EVENT

from config import *
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.battle.container import BattleContainer
from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.text.text import Text
from classes.text.dynamic_text import DynamicText

from constants import BOSS_ACT_EFFECT


class ActMenu(BattleMenu):
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

        self.runtime_counter = 0  # Previnir que entre clicando nos itens

        self.items_per_column = 5  # Quantas opções pode ter por coluna

        self.showing_act_response = False  # Controla quando mostra o texto das respostas
        self.act_response_to_show = 0  # Indice que indica qual resposta deve ser mostrada
        self.selected_responses = []  # Variável auxiliar com os textos que vão ser exibidos
        self.response_text = DynamicText('', FontManager.fonts['Gamer'], 20, int((450*100)/self.display.get_height()), 0, sound='text_2.wav')
        self.start_showing_text = False
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        self.selected_option = (self.selected_option+increment)%len(self.__options)
    
    def on_first_execution(self):
        self.runtime_counter += 1
        EventManager.clear()

    def update(self):
        if self.runtime_counter == 0:
            self.on_first_execution()

        keys = pygame.key.get_pressed()  # Pegando o dicinoário das teclas

        # Bloco que executa se eu não tiver selecionado nenhuma opção
        if not self.showing_act_response:
            # Ajusto o cursor
            self.cursor_rect.center = self.__options[self.selected_option%len(self.__options)]['text'].rect.center
            self.cursor_rect.right = self.__options[self.selected_option%len(self.__options)]['text'].rect.left

            # Movendo o cursor pelos itens do inventário
            for event in EventManager.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.move_cursor(1)
                        SoundManager.play_sound('squeak.wav')
                    elif event.key == pygame.K_UP:
                        self.move_cursor(-1)
                        SoundManager.play_sound('squeak.wav')
                    elif event.key == pygame.K_LEFT:
                        self.move_cursor(-self.items_per_column)
                        SoundManager.play_sound('squeak.wav')
                    elif event.key == pygame.K_RIGHT:
                        self.move_cursor(self.items_per_column)
                        SoundManager.play_sound('squeak.wav')
                         
                    # Selecionando um item
                    if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and 0 <= self.selected_option < len(self.__options):
                        self.selected_responses = self.__options[self.selected_option]['responses']
                        self.showing_act_response = True
                        self.entered_pressing = True
                        self.act_response_to_show = 0
                        self.start_showing_text = True
                        pygame.event.post(pygame.event.Event(BOSS_ACT_EFFECT, {
                            'effect': self.__options[self.selected_option]['effect']
                        }))
                        SoundManager.play_sound('select.wav')

            # Volto no menu anterior
            if keys[pygame.K_x] or keys[pygame.K_BACKSPACE]:  # Para eu voltar no menu anterior
                BattleMenuManager.go_back()
        else:
            self.response_text.max_length = self.container.inner_rect.width

            if self.start_showing_text:
                self.response_text.restart(self.selected_responses[self.act_response_to_show])
                self.start_showing_text = False

            for event in EventManager.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                        if not self.response_text.finished:
                            self.response_text.skip_text()
                        else:
                            self.act_response_to_show += 1
                            self.start_showing_text = True

                            if self.act_response_to_show+1 > len(self.selected_responses):
                                pygame.event.post(pygame.event.Event(BOSS_TURN_EVENT))
                                self.showing_act_response = False

            self.response_text.update()
            self.response_text.position = (
                self.container.inner_rect.x + 10,
                self.container.inner_rect.y + 10,
            )
        
        # Evitando que eu selecione vários itens ao mesmo tempo
        if not keys[pygame.K_z] and not keys[pygame.K_RETURN]:
            self.entered_pressing = False

    def draw(self):
        if not self.showing_act_response:
            column = 0
            for i, opt in enumerate(self.__options):
                if i >= self.items_per_column:
                    column = 1
                
                opt['text'].rect.x = self.container.inner_rect.x + 10*abs(column-1) + self.container.inner_rect.width*column/2 + (1 - 2*column)*self.cursor_rect.width
                opt['text'].rect.y = self.container.inner_rect.y + opt['text'].rect.height*(i)

                opt['text'].draw(self.display)
            
            self.display.blit(self.cursor, self.cursor_rect)
        else:
            self.response_text.draw(self.display)

    
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value: list[dict]):
        for option in value:
            self.__options.append({
                'text': Text(f'* {option['label']}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                **option
            })

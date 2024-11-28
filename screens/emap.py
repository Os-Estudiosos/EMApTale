import pygame
import os

from screens import State

from config import *
from config.savemanager import SaveManager
from config.globalmanager import GlobalManager

from classes.map.interaction import InteractionManager
from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk

class EMAp(State):
    def __init__(self, name, display):
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display
        self.__execution_counter = 0

        self.items_group = pygame.sprite.Group()
        GlobalManager.groups['items'] = self.items_group

        # Inicializa o loader do mapa
        self.map_loader = MapLoader(os.path.join(GET_PROJECT_PATH(), 'tileset', 'emap.tmx'))
        self.map_loaded = False

        # Inicializa o jogador
        self.player = Frisk(self.map_loader.walls)

        # Configura a câmera com as dimensões do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = self.__display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)
        GlobalManager.set_camera(self.camera)

        # Inicializa o InteractionManager
        chatbox = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'chatbox.png'))
        tecla_z_image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'tecla_z.png'))

        # Redimensiona a chatbox
        new_width = chatbox.get_width() + 1100  # Ajuste personalizado
        new_height = chatbox.get_height() + 250
        chatbox = pygame.transform.scale(chatbox, (new_width, new_height))

        # Redimensiona a imagem da tecla "Z"
        tecla_z_image = pygame.transform.scale(tecla_z_image, (70, 70))

        # Inicializa o InteractionManager
        self.interaction_manager = InteractionManager(
            self.player, chatbox, tecla_z_image
        )
        self.interaction_manager.set_chatbox_position((
            (self.__display.get_width() - new_width) // 2,  # Centraliza horizontalmente
            self.__display.get_height() - new_height        # Posiciona no rodapé
        ))

    def on_first_execution(self):
        SaveManager.load()
        GlobalManager.load_infos()
        self.map_loader.load_items()
        self.map_loaded = True

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        # Limpa a tela
        self.__display.fill((0, 0, 0))

        # Atualiza a posição da câmera para seguir o jogador
        self.camera.update(self.player.rect)

        # Renderiza os tiles do mapa
        self.map_loader.render_with_vector(self.__display, self.camera, MAP_OFFSET_VECTOR)

        # Coleta e ordena os objetos renderizáveis (incluindo o jogador)
        renderables = self.map_loader.get_renderables(self.player)
        renderables = self.camera.apply_ysort(renderables)

        self.items_group.update()
        self.items_group.draw(self.__display)

        # Renderiza os objetos na ordem correta
        for _, image, rect in renderables:
            if isinstance(image, pygame.Surface):
                self.__display.blit(image, rect)
            elif isinstance(image, Frisk):
                image.draw(self.__display, self.camera)

        # Captura eventos e gerencia interações
        self.interaction_manager.check_interaction()
        self.interaction_manager.handle_interaction()
        self.interaction_manager.render_interaction(self.__display)

        # Atualiza a movimentação do jogador
        if not self.interaction_manager.dynamic_text:
            keys = pygame.key.get_pressed()
            self.player.move(self.camera, keys)

        # Atualiza a tela
        pygame.display.flip()

    def on_last_execution(self):
        self.__execution_counter = 0
    
    @property
    def execution_counter(self):
        return self.__execution_counter

    @property
    def display(self):
        return self.__display
    
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

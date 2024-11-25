import pygame
import os
from config.savemanager import SaveManager

from classes.map.interaction import InteractionManager
from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk

class EMAp:
    def __init__(self, name, display, game_state_manager):
        self.__name = name
        self.__display = display  # Exemplo: 800x600 em modo janela
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        # Inicializa o loader do mapa
        self.map_loader = MapLoader(os.path.join('tileset', 'emap.tmx'))
        self.map_loaded = False

        # Inicializa o jogador
        self.player = Frisk(self.map_loader.walls)

        # Configura a câmera com as dimensões do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = self.__display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)

        # Inicializa o InteractionManager
        chatbox = pygame.image.load(os.path.join('sprites', 'hud', 'chatbox.png'))
        tecla_z_image = pygame.image.load(os.path.join('sprites', 'hud', 'tecla_z.png'))

        # Redimensiona a chatbox
        new_width = chatbox.get_width() + 1100  # Ajuste personalizado
        new_height = chatbox.get_height() + 250
        chatbox = pygame.transform.scale(chatbox, (new_width, new_height))

        # Redimensiona a imagem da tecla "Z"
        tecla_z_image = pygame.transform.scale(tecla_z_image, (50, 50))

        # Inicializa o InteractionManager
        self.interaction_manager = InteractionManager(
            self.map_loader.interactions, self.player, chatbox, tecla_z_image
        )
        self.interaction_manager.set_chatbox_position((
            (self.__display.get_width() - new_width) // 2,  # Centraliza horizontalmente
            self.__display.get_height() - new_height        # Posiciona no rodapé
        ))

    def on_first_execution(self):
        SaveManager.load()
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
        self.map_loader.render_with_vector(self.__display, self.camera, self.map_loader.offset_vector)

        # Coleta e ordena os objetos renderizáveis (incluindo o jogador)
        renderables = self.map_loader.get_renderables(self.player)
        renderables = self.camera.apply_ysort(renderables)

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

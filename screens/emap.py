import pygame
from pygame.font import Font
import os

from config.savemanager import SaveManager

from classes.map.interaction import InteractionManager
from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk
from classes.text.dynamic_text import DynamicText

class EMAp:
    def __init__(self, name, display, game_state_manager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        # Inicializa o loader do mapa
        self.map_loader = MapLoader(os.path.join('tileset', 'emap.tmx'))
        self.map_loaded = False

        # Inicializa o jogador
        self.player = Frisk(self.map_loader.walls)

        # Inicializa o InteractionManager
        self.interaction_manager = InteractionManager(self.map_loader.interactions, self.player)

        # Configura a câmera com as dimensões do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)

        # Inicializa um objeto DynamicText (será reutilizado)
        self.dynamic_text = None

        # Carrega a imagem da caixa de texto sem redimensionar
        self.chatbox = pygame.image.load(os.path.join('sprites', 'hud', 'chatbox.png'))

        # Obtém as dimensões da caixa de texto
        chatbox_width, chatbox_height = self.chatbox.get_size()

        # Calcula a posição para centralizar horizontalmente na parte inferior
        self.chatbox_position = (
            (self.__display.get_width() - chatbox_width) // 2,  # Centraliza horizontalmente
            self.__display.get_height() - chatbox_height       # Posiciona no rodapé
        )

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

        # Renderiza as áreas de interação
        self.interaction_manager.draw(self.__display, self.camera)

        # Desenha a caixa de texto
        self.__display.blit(self.chatbox, self.chatbox_position)


        # Define o vetor de deslocamento
        vector = pygame.math.Vector2(-100, -150)

        # Renderiza todos os tiles como camada de fundo (fundo estático)
        for layer in self.map_loader.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        pos = (
                            x * self.map_loader.tmx_data.tilewidth * self.map_loader.scale_factor + vector.x,
                            y * self.map_loader.tmx_data.tileheight * self.map_loader.scale_factor + vector.y
                        )
                        scaled_tile = pygame.transform.scale(tile, (
                            int(tile.get_width() * self.map_loader.scale_factor),
                            int(tile.get_height() * self.map_loader.scale_factor)
                        ))
                        rect = pygame.Rect(*pos, scaled_tile.get_width(), scaled_tile.get_height())
                        self.__display.blit(scaled_tile, self.camera.apply(rect))

        # Lista unificada de renderizáveis para ordenação
        renderables = []

        # Adiciona objetos com GID à lista de renderizáveis
        for layer in self.map_loader.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:
                    tile_image = self.map_loader.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        pos = (
                            obj.x * self.map_loader.scale_factor + vector.x,
                            obj.y * self.map_loader.scale_factor + vector.y
                        )
                        scaled_image = pygame.transform.scale(tile_image, (
                            int(tile_image.get_width() * self.map_loader.scale_factor),
                            int(tile_image.get_height() * self.map_loader.scale_factor)
                        ))
                        rect = pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())
                        renderables.append((rect.bottom, scaled_image, rect))

        # Adiciona o jogador à lista de renderizáveis
        renderables.append((self.player.rect.bottom, self.player, self.player.rect))

        # Ordena os objetos localmente pela coordenada Y (base inferior)
        renderables.sort(key=lambda item: item[0])

        # Renderiza todos os objetos e o jogador na ordem correta
        for _, image, rect in renderables:
            if isinstance(image, pygame.Surface):
                self.__display.blit(image, self.camera.apply(rect))
            elif isinstance(image, Frisk):
                image.draw(self.__display, self.camera)

        # Verifica interações
        keys = pygame.key.get_pressed()
        interaction = self.interaction_manager.check_interaction(keys)

        if interaction and not self.dynamic_text:
            # Define o texto dinâmico
            self.dynamic_text = DynamicText(
                text=f"Texto para {interaction['interaction_name']}: {interaction['value']}",
                font="fonts/Gamer.ttf",  # Ajuste para sua fonte real
                letters_per_second=20,  # Velocidade do texto
                text_size=24,
                position=(self.chatbox_position[0] + 20, self.chatbox_position[1] + 20),  # Dentro da caixa
                color=(255, 255, 255),
                max_length= 250
            )
        elif not interaction:
            self.dynamic_text = None  # Remove texto se não houver interação

        # Desenha a caixa de texto e o texto dinâmico
        if self.dynamic_text:
            # Desenha a caixa de texto
            self.__display.blit(self.chatbox, self.chatbox_position)

            # Atualiza e desenha o texto
            self.dynamic_text.update()
            self.dynamic_text.draw(self.__display)

        # Atualiza a movimentação do jogador
        self.player.move(self.camera, keys)

        # Atualiza a tela
        pygame.display.flip()

    def on_last_execution(self):
        self.__execution_counter = 0

import pygame
import os

from config.savemanager import SaveManager

from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk

class EMAp:
    def __init__(self, name, display, game_state_manager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        # Inicializa o loader do mapa e o jogador
        self.map_loader = MapLoader(os.path.join('tileset', 'emap.tmx'))
        self.map_loaded = False
        self.player = Frisk(self.map_loader.walls)

        # Configura a câmera com as dimensões do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)

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

        # Atualiza a movimentação do jogador
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
    def game_state_manager(self):
        return self.__game_state_manager

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

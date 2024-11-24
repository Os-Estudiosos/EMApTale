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
        self.__display = display  # Exemplo: 800x600 em modo janela

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
        screen_width, screen_height = self.__display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)

        # Inicializa um objeto DynamicText (será reutilizado)
        self.dynamic_text = None

        # Carrega a imagem da caixa de texto
        self.chatbox = pygame.image.load(os.path.join('sprites', 'hud', 'chatbox.png'))

        new_width = self.chatbox.get_width() + 1100 # Aumenta a largura em 100 pixels
        new_height = self.chatbox.get_height() + 250  # Aumenta a altura em 50 pixels

        # Redimensiona a caixa
        self.chatbox = pygame.transform.scale(self.chatbox, (new_width, new_height))

        # Atualiza a posição da caixa para centralizar
        self.chatbox_position = (
            (self.__display.get_width() - new_width) // 2,  # Centraliza horizontalmente
            self.__display.get_height() - new_height       # Posiciona no rodapé
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

        # Renderiza os tiles do mapa
        vector = pygame.math.Vector2(-100, -150)
        for layer in self.map_loader.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        pos = (
                            x * self.map_loader.tmx_data.tilewidth * self.map_loader.scale_factor + vector.x,
                            y * self.map_loader.tmx_data.tileheight * self.map_loader.scale_factor + vector.y
                        )
                        scaled_tile = pygame.transform.scale(
                            tile,
                            (int(tile.get_width() * self.map_loader.scale_factor),
                            int(tile.get_height() * self.map_loader.scale_factor))
                        )
                        rect = pygame.Rect(*pos, scaled_tile.get_width(), scaled_tile.get_height())
                        self.__display.blit(scaled_tile, self.camera.apply(rect))

        # Renderiza os objetos e o jogador
        renderables = []
        for layer in self.map_loader.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:
                    tile_image = self.map_loader.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        pos = (
                            obj.x * self.map_loader.scale_factor + vector.x,
                            obj.y * self.map_loader.scale_factor + vector.y
                        )
                        scaled_image = pygame.transform.scale(
                            tile_image,
                            (int(tile_image.get_width() * self.map_loader.scale_factor),
                            int(tile_image.get_height() * self.map_loader.scale_factor))
                        )
                        rect = pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())
                        renderables.append((rect.bottom, scaled_image, rect))

        # Adiciona o jogador à lista de renderizáveis
        renderables.append((self.player.rect.bottom, self.player, self.player.rect))

        # Ordena e renderiza os objetos corretamente
        renderables.sort(key=lambda item: item[0])
        for _, image, rect in renderables:
            if isinstance(image, pygame.Surface):
                self.__display.blit(image, self.camera.apply(rect))
            elif isinstance(image, Frisk):
                image.draw(self.__display, self.camera)

        # Verifica interações
        keys = pygame.key.get_pressed()
        interaction = self.interaction_manager.check_interaction(keys)

        if interaction and not self.dynamic_text:
            # Cria o texto dinâmico
            self.dynamic_text = DynamicText(
                text=f"{interaction['value']}",
                font="fonts/Gamer.ttf",
                letters_per_second=20,
                text_size=50,
                position=(
                    self.chatbox_position[0] + 20,  # Margem lateral
                    self.chatbox_position[1] + 20  # Margem superior
                ),
                color=(255, 255, 255),
                max_length=self.chatbox.get_width() - 40
            )
        elif not interaction:
            # Remove o texto dinâmico quando não há interação
            self.dynamic_text = None

        # Renderiza a caixa de texto e o texto dinâmico apenas se houver interação ativa
        if self.dynamic_text:
            self.__display.blit(self.chatbox, self.chatbox_position)  # Renderiza o chatbox
            self.dynamic_text.update()  # Atualiza o texto dinâmico
            self.dynamic_text.draw(self.__display)  # Desenha o texto dinâmico

        # Atualiza a movimentação do jogador
        self.player.move(self.camera, keys)

        # Captura de tela (pressione F12 para salvar)
        if keys[pygame.K_F12]:
            pygame.image.save(self.__display, "screenshot.png")
            print("Screenshot salva como 'screenshot.png'")


        # Atualiza a tela
        pygame.display.flip()


    def on_last_execution(self):
        self.__execution_counter = 0
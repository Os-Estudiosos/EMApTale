import pygame
from screens import State
from config import *
from config.gamestatemanager import GameStateManager
from config.savemanager import SaveManager
from pytmx import load_pygame

# Classe MapLoader para carregar e renderizar o mapa .tmx
class MapLoader:
    def __init__(self, map_file):
        # Carrega o mapa usando o pytmx
        self.tmx_data = load_pygame(map_file)

    def render(self, surface):
        # Renderiza cada camada do mapa na superfície fornecida
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                # Renderiza cada tile da camada usando suas coordenadas
                for x, y, tile in layer.tiles():
                    if tile:  # Verifica se há uma imagem de tile associada
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    
    def get_size(self):
        # Retorna o tamanho do mapa em pixels
        width = self.tmx_data.width * self.tmx_data.tilewidth
        height = self.tmx_data.height * self.tmx_data.tileheight
        return width, height

# Classe EMAp que representa a cena do mapa
class EMAp(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        game_state_manager: GameStateManager,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__name = name
        self.__display: pygame.Surface = display
        self.__game_state_manager: GameStateManager = game_state_manager
        self.__execution_counter = 0

        # Inicialize o MapLoader com o caminho do mapa
        self.map_loader = MapLoader('tileset/emap.tmx')
        self.map_loaded = False  # Flag para indicar que o mapa foi carregado

    def on_first_execution(self):
        # Qualquer inicialização extra para o primeiro frame
        self.map_loaded = True  # Define o flag para indicar que o mapa foi carregado

    def run(self):
        # Verifica se é a primeira execução e chama on_first_execution se necessário
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        # Limpa a tela antes de desenhar o mapa
        self.__display.fill((0, 0, 0))  # Fundo preto

        # Renderiza o mapa na tela
        self.map_loader.render(self.__display)
    
    def on_last_execution(self):
        # Reseta o contador de execução
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

import pygame
import os
from screens import State

from config import *

from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk

#Gerencia o estado e a lógica do jogo
class EMAp(State):
    #Inicializa o estado do jogo com nome, display e gerenciador de estado
    def __init__(self, name, display, game_state_manager):
        self.__name = name  
        self.__display = display  #Display para renderização
        self.__game_state_manager = game_state_manager  
        self.__execution_counter = 0  #Contador de execuções do estado

        #Inicializa o MapLoader e carrega o mapa
        self.map_loader = MapLoader(os.path.join(GET_PROJECT_PATH(), 'tileset', 'emap.tmx'))
        self.map_loaded = False  #Marca que o mapa não foi carregado ainda
        self.player = Frisk(self.map_loader.walls)  #Inicializa o jogador com as áreas de colisão

        #Obtém o tamanho do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = display.get_size()
        
        #Inicializa a câmera com as dimensões do mapa e da tela
        self.camera = Camera(map_width, map_height, screen_width, screen_height)

    #Método para ser executado na primeira execução do estado
    def on_first_execution(self):
        self.map_loaded = True  #Marca que o mapa foi carregado

    #Método principal de execução do estado
    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        self.__display.fill((0, 0, 0))

        # Atualiza a posição da câmera para seguir o jogador
        self.camera.update(self.player.rect)

        # Define o vetor de deslocamento para ajustar a posição dos tiles
        vector = pygame.math.Vector2(-100, -150)

        # Renderiza o mapa com o deslocamento aplicado
        self.map_loader.render_with_vector(self.__display, self.camera, vector)

        # Renderiza objetos específicos no mapa
        self.map_loader.render_objects_with_gid(self.__display, self.camera, vector)

        # Atualiza e desenha o jogador na tela
        keys = pygame.key.get_pressed()
        self.player.move(self.camera, keys)
        self.player.draw(self.__display, self.camera)
        
        pygame.display.flip()

    #Método para resetar o contador de execução ao sair do estado
    def on_last_execution(self):
        self.__execution_counter = 0

    # Propriedade para obter o contador de execução
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
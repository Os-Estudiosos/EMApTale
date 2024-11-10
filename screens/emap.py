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

        # Inicialização do jogador
        self.player = Player()  # Instância da classe Player, definida abaixo

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
        
        # Atualiza e desenha o jogador
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw(self.__display)
        
        # Atualiza a tela
        pygame.display.flip()

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

import pygame

class Player:
    def __init__(self):
        # Carregar o sprite sheet do player na pasta sprites/player/frisk.png
        self.sprite_sheet = pygame.image.load('sprites/player/frisk.png').convert_alpha()
        
        # Configuração dos frames e direções
        self.frame_width = 24
        self.frame_height = 34

        # Ajustado para 2 colunas e 4 linhas com base no layout do sprite sheet
        self.cols = 2
        self.rows = 4

        # Dividir o sprite sheet em frames
        self.frames = self.load_frames()

        # Configurações de animação e posição
        self.x, self.y = 100, 100  # Posição inicial do jogador
        self.direction = 0  # 0: Baixo, 1: Esquerda, 2: Cima, 3: Direita
        self.frame_index = 0
        self.frame_delay = 10  # Velocidade da animação
        self.frame_counter = 0

    def load_frames(self):
        # Função para dividir o sprite sheet em frames, sem uma verificação rígida
        frames = []
        for row in range(self.rows):
            direction_frames = []
            for col in range(self.cols):
                # Calcule as coordenadas x e y para cada frame
                x = col * self.frame_width
                y = row * self.frame_height

                # Certifique-se de que estamos dentro dos limites do sprite sheet antes de cortar o frame
                if x + self.frame_width <= self.sprite_sheet.get_width() and y + self.frame_height <= self.sprite_sheet.get_height():
                    frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                    direction_frames.append(frame)
            # Adiciona a lista de frames da direção apenas se contiver frames
            if direction_frames:
                frames.append(direction_frames)
        return frames

    def update_animation(self):
        # Verifica se `self.direction` está dentro dos limites de `self.frames`
        if self.direction < len(self.frames):
            # Garante que `self.frame_index` esteja dentro dos limites da sublista atual
            self.frame_index = self.frame_index % len(self.frames[self.direction])

            # Atualiza o frame da animação
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])

    def move(self, keys):
        # Ajusta `self.direction` e a posição de acordo com a tecla pressionada
        if keys[pygame.K_DOWN]:
            self.y += 2
            self.direction = 0  # Linha 0 é para movimento para baixo
        elif keys[pygame.K_LEFT]:
            self.x -= 2
            self.direction = 1  # Linha 1 é para movimento para a esquerda
        elif keys[pygame.K_UP]:
            self.y -= 2
            self.direction = 2  # Linha 2 é para movimento para cima
        elif keys[pygame.K_RIGHT]:
            self.x += 2
            self.direction = 3  # Linha 3 é para movimento para a direita
        else:
            self.frame_index = 0  # Frame neutro quando parado

        # Se qualquer tecla de movimento estiver pressionada, atualiza a animação
        if any([keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP]]):
            self.update_animation()

    def draw(self, surface):
        # Verifica se `self.direction` e `self.frame_index` estão dentro dos limites antes de desenhar
        if self.direction < len(self.frames) and self.frame_index < len(self.frames[self.direction]):
            surface.blit(self.frames[self.direction][self.frame_index], (self.x, self.y))

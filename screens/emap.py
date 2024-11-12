import pygame
from screens import State
from config.gamestatemanager import GameStateManager
from pytmx import load_pygame

class MapLoader:
    def __init__(self, map_file):
        # Carrega o mapa usando o pytmx
        self.tmx_data = load_pygame(map_file)
        # Armazena as áreas de colisão
        self.walls = self.load_walls()

    def load_walls(self):
        # Carrega áreas de colisão da camada "WallsColider"
        walls = []
        for layer in self.tmx_data.layers:
            if layer.name == "WallsColider":
                for obj in layer:
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    walls.append(rect)
        return walls

    def render(self, surface):
        # Renderiza cada camada do mapa na superfície fornecida
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def get_size(self):
        # Retorna o tamanho do mapa em pixels
        width = self.tmx_data.width * self.tmx_data.tilewidth
        height = self.tmx_data.height * self.tmx_data.tileheight
        return width, height

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

        # Inicializa o MapLoader com o caminho do mapa
        self.map_loader = MapLoader('tileset/emap.tmx')
        self.map_loaded = False

        # Inicialização do jogador
        self.player = Player(self.map_loader.walls)

    def on_first_execution(self):
        self.map_loaded = True

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        self.__display.fill((0, 0, 0))

        # Renderiza o mapa na tela
        self.map_loader.render(self.__display)
        
        # Atualiza e desenha o jogador
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw(self.__display)
        
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

class Player:
    def __init__(self, walls):
        # Carregar o sprite sheet do player
        self.sprite_sheet = pygame.image.load('sprites/player/frisk.png').convert_alpha()
        
        # Configuração dos frames e direções
        self.frame_width = 24
        self.frame_height = 34
        self.cols = 2
        self.rows = 4
        self.frames = self.load_frames()

        # Configurações de animação e posição
        self.x, self.y = 100, 200
        self.direction = 0
        self.frame_index = 0
        self.frame_delay = 10
        self.frame_counter = 0

        # Referência das paredes para colisão
        self.walls = walls

    def load_frames(self):
        frames = []
        for row in range(self.rows):
            direction_frames = []
            for col in range(self.cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                direction_frames.append(frame)
            if direction_frames:
                frames.append(direction_frames)
        return frames

    def update_animation(self):
        if self.direction < len(self.frames):
            self.frame_index = self.frame_index % len(self.frames[self.direction])
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])

    def move(self, keys):
        old_x, old_y = self.x, self.y

        # Movimenta o player
        if keys[pygame.K_DOWN]:
            self.y += 2
            self.direction = 0
        elif keys[pygame.K_LEFT]:
            self.x -= 2
            self.direction = 1
        elif keys[pygame.K_UP]:
            self.y -= 2
            self.direction = 2
        elif keys[pygame.K_RIGHT]:
            self.x += 2
            self.direction = 3
        else:
            self.frame_index = 0

        player_rect = pygame.Rect(self.x, self.y, self.frame_width, self.frame_height)

        # Checa colisão
        if any(player_rect.colliderect(wall) for wall in self.walls):
            self.x, self.y = old_x, old_y

        if any([keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP]]):
            self.update_animation()

    def draw(self, surface):
        if self.direction < len(self.frames) and self.frame_index < len(self.frames[self.direction]):
            surface.blit(self.frames[self.direction][self.frame_index], (self.x, self.y))

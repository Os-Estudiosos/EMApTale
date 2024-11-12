import pygame
import math
from screens import State
from config.gamestatemanager import GameStateManager
from pytmx import load_pygame
from utils import sign


#Controla a área visível do mapa em relação ao jogador
class Camera:
    #Inicializa a câmera com as dimensões do mapa e da tela
    def __init__(self, map_width, map_height, screen_width, screen_height):
        self.map_width = map_width  #Largura total do mapa
        self.map_height = map_height  #Altura total do mapa
        self.screen_width = screen_width  #Largura da tela de exibição
        self.screen_height = screen_height  #Altura da tela de exibição
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)  #Define a área da câmera

    #Método para aplicar a posição da câmera a uma entidade, ajustando sua posição
    def apply(self, entity):
        #Verifica se a entidade é um retângulo (pygame.Rect)
        if isinstance(entity, pygame.Rect):
            #Move a entidade com base na posição da câmera, retornando a posição ajustada
            return entity.move(-self.camera_rect.x, -self.camera_rect.y)
        #Se a entidade não for pygame.Rect, usa a propriedade rect para mover
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    #Método para atualizar a posição da câmera em relação ao jogador
    def update(self, target_rect):
        #Centraliza a câmera no centro do jogador (target_rect)
        x = target_rect.centerx - self.screen_width // 2
        y = target_rect.centery - self.screen_height // 2

        #Limita a câmera para que ela não saia dos limites do mapa
        x = max(0, min(x, self.map_width - self.screen_width))
        y = max(0, min(y, self.map_height - self.screen_height))

        #Atualiza a posição da câmera com a nova posição calculada
        self.camera_rect = pygame.Rect(x, y, self.screen_width, self.screen_height)

#Carrega e renderiza mapas do tipo .tmx
class MapLoader:
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)  # Carrega o mapa usando pytmx
        self.scale_factor = 2.5  # Fator de escala para o mapa e colisões
        self.offset_vector = pygame.math.Vector2(-100, -150)  # Deslocamento dos blocos de colisão
        self.walls = self.load_walls()  # Carrega as áreas de colisão do mapa

    def render_with_vector(self, surface, camera, vector):
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        pos = (
                            x * self.tmx_data.tilewidth * self.scale_factor + vector.x,
                            y * self.tmx_data.tileheight * self.scale_factor + vector.y
                        )
                        surface.blit(
                            pygame.transform.scale_by(tile, self.scale_factor),
                            camera.apply(pygame.Rect(*pos, self.tmx_data.tilewidth * self.scale_factor, self.tmx_data.tileheight * self.scale_factor))
                        )

    def render_objects_with_gid(self, surface, camera, vector):
        """
        Renderiza objetos com gid definido no mapa.
        """
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:  # Verifica se o objeto tem gid e está visível
                    # Obtém a imagem do objeto a partir do gid
                    tile_image = self.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        # Aplica o fator de escala e deslocamento
                        pos = (
                            obj.x * self.scale_factor + vector.x,
                            obj.y * self.scale_factor + vector.y
                        )
                        scaled_image = pygame.transform.scale_by(tile_image, self.scale_factor)
                        surface.blit(scaled_image, camera.apply(pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())))

    def load_walls(self):
        walls = []
        for layer in self.tmx_data.layers:
            if layer.name == "WallsColider":
                for obj in layer:
                    # Escala e aplica o deslocamento às áreas de colisão
                    rect = pygame.Rect(
                        obj.x * self.scale_factor + self.offset_vector.x,
                        obj.y * self.scale_factor + self.offset_vector.y,
                        obj.width * self.scale_factor,
                        obj.height * self.scale_factor
                    )
                    walls.append(rect)
        return walls

    def get_size(self):
        width = self.tmx_data.width * self.tmx_data.tilewidth * self.scale_factor
        height = self.tmx_data.height * self.tmx_data.tileheight * self.scale_factor
        return width, height

#Gerencia o estado e a lógica do jogo
class EMAp(State):
    #Inicializa o estado do jogo com nome, display e gerenciador de estado
    def __init__(self, name, display, game_state_manager):
        self.__name = name  
        self.__display = display  #Display para renderização
        self.__game_state_manager = game_state_manager  
        self.__execution_counter = 0  #Contador de execuções do estado

        #Inicializa o MapLoader e carrega o mapa
        self.map_loader = MapLoader('tileset/emap.tmx')
        self.map_loaded = False  #Marca que o mapa não foi carregado ainda
        self.player = Player(self.map_loader.walls)  #Inicializa o jogador com as áreas de colisão

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
        self.player.move(keys)
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

#Gerencia o jogador, incluindo animação, movimento e colisões
class Player:
    def __init__(self, walls):
        self.sprite_sheet = pygame.image.load('sprites/player/frisk.png').convert_alpha()  # Carrega a imagem do jogador
        self.frame_width = 24  # Largura de cada quadro de animação
        self.frame_height = 34  # Altura de cada quadro de animação
        self.cols = 2  # Número de colunas na folha de sprites
        self.rows = 4  # Número de linhas na folha de sprites
        self.scale_factor = 2.5  # Fator de escala para o jogador
        self.frames = self.load_frames()
        self.x, self.y = 150, 350  # Posição inicial do jogador
        self.direction = 0  # Direção inicial do jogador
        self.frame_index = 0  # Índice do quadro atual de animação
        self.frame_delay = 10  # Tempo de atraso entre quadros de animação
        self.frame_counter = 0  # Contador para controlar o atraso
        self.walls = walls  # Lista de retângulos de colisão
        self.rect = pygame.Rect(self.x, self.y, self.frame_width * self.scale_factor, self.frame_height * self.scale_factor)
        self.mask = None  # Máscara para colisão precisa

    def load_frames(self):
        frames = []
        for row in range(self.rows):
            direction_frames = []
            for col in range(self.cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                
                # Escala o quadro para 2.5x o tamanho original
                scaled_frame = pygame.transform.scale(
                    frame, (int(self.frame_width * self.scale_factor), int(self.frame_height * self.scale_factor))
                )
                
                direction_frames.append(scaled_frame)  # Adiciona o quadro escalado à direção atual
            frames.append(direction_frames)  # Adiciona os quadros da direção à lista principal
        return frames

    def update_animation(self):
        if self.direction < len(self.frames):
            self.frame_index = self.frame_index % len(self.frames[self.direction])
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
                
            # Atualiza a máscara para o quadro atual
            self.update_mask()

    def update_mask(self):
        # Atualiza a máscara do jogador com o quadro de animação atual
        current_frame = self.frames[self.direction][self.frame_index]
        self.mask = pygame.mask.from_surface(current_frame)

    def update_dir(self, direction):
        if direction.x > 0:
            self.direction = 3  # Direita
        elif direction.x < 0:
            self.direction = 1  # Esquerda
        elif direction.y > 0:
            self.direction = 0  # Baixo
        elif direction.y < 0:
            self.direction = 2  # Cima

    def move(self, keys):
        old_rect = self.rect.copy()
        base_speed = 10

        direction = pygame.math.Vector2(
            sign((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) or (keys[pygame.K_d] - keys[pygame.K_a])),
            sign((keys[pygame.K_DOWN] - keys[pygame.K_UP]) or (keys[pygame.K_s] - keys[pygame.K_w]))
        )

        if direction.length() != 0:
            direction = direction.normalize()

        # Movimenta o jogador
        self.rect.x += base_speed * direction.x
        self.rect.y += base_speed * direction.y

        # Verifica colisão de máscara com as paredes
        if self.check_wall_collisions():
            # Se colidir, reverte para a posição anterior
            self.rect = old_rect
        else:
            # Atualiza a posição armazenada de self.x e self.y
            self.x, self.y = self.rect.topleft

        # Atualiza a direção e a animação
        self.update_dir(direction)
        if direction.length() != 0:
            self.update_animation()

    def check_wall_collisions(self):
        """
        Verifica colisão de máscara entre o jogador e as paredes.
        """
        if self.mask is None:
            return False

        for wall in self.walls:
            wall_mask = pygame.mask.Mask((wall.width, wall.height), fill=True)
            offset = (wall.x - self.rect.x, wall.y - self.rect.y)

            # Verifica colisão pixel a pixel
            if self.mask.overlap(wall_mask, offset):
                return True
        return False

    def draw(self, surface, camera):
        if self.direction < len(self.frames) and self.frame_index < len(self.frames[self.direction]):
            frame_image = self.frames[self.direction][self.frame_index]
            surface.blit(frame_image, camera.apply(self.rect))

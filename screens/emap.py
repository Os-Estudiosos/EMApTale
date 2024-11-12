import pygame
from screens import State
from config.gamestatemanager import GameStateManager
from pytmx import load_pygame

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

#Carrega e renderiza mapas do tipo `.tmx`
class MapLoader:
    #Inicializa o mapa com o arquivo especificado
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)  #Carrega o mapa usando `pytmx`
        self.walls = self.load_walls()  #Carrega as áreas de colisão do mapa

    #Método para carregar as áreas de colisão do mapa a partir da camada "WallsColider"
    def load_walls(self):
        walls = []  
        for layer in self.tmx_data.layers:  
            if layer.name == "WallsColider":  
                for obj in layer:  
                    #Cria um retângulo de colisão e o adiciona à lista de paredes
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    walls.append(rect)
        return walls  

    #Método para renderizar o mapa na tela, considerando a posição da câmera
    def render(self, surface, camera):
        #Percorre cada camada do mapa para renderização
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):  
                for x, y, tile in layer.tiles():  # Para cada tile na camada
                    if tile:  
                        #Calcula a posição do tile no mapa com base no tamanho
                        pos = (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        #Renderiza o tile na tela ajustado pela câmera
                        surface.blit(
                            tile,
                            camera.apply(pygame.Rect(*pos, self.tmx_data.tilewidth, self.tmx_data.tileheight))
                            )

    # Método para obter o tamanho total do mapa em pixels
    def get_size(self):
        width = self.tmx_data.width * self.tmx_data.tilewidth  # Calcula a largura total do mapa
        height = self.tmx_data.height * self.tmx_data.tileheight  # Calcula a altura total do mapa
        return width, height  # Retorna as dimensões do mapa

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
        #Verifica se é a primeira execução e chama `on_first_execution`
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        self.__display.fill((0, 0, 0)) 

        #Atualiza a posição da câmera para seguir o jogador
        self.camera.update(self.player.rect)

        #Renderiza o mapa considerando o deslocamento da câmera
        self.map_loader.render(self.__display, self.camera)
        
        #Atualiza e desenha o jogador na tela
        keys = pygame.key.get_pressed()  # btém o estado atual das teclas
        self.player.move(keys)  #Move o jogador com base nas teclas pressionadas
        self.player.draw(self.__display, self.camera)  #Desenha o jogador ajustado pela câmera
        
        pygame.display.flip()  #Atualiza a tela com as alterações

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
    #Inicializa o jogador com áreas de colisão e configurações de animação
    def __init__(self, walls):
        self.sprite_sheet = pygame.image.load('sprites/player/frisk.png').convert_alpha()  # Carrega a imagem do jogador
        self.frame_width = 24  # Largura de cada quadro de animação
        self.frame_height = 34  # Altura de cada quadro de animação
        self.cols = 2  # Número de colunas na folha de sprites
        self.rows = 4  # Número de linhas na folha de sprites
        self.frames = self.load_frames() 
        self.x, self.y = 100, 200  #Posição inicial do jogador
        self.direction = 0  #Direção inicial do jogador
        self.frame_index = 0  #Índice do quadro atual de animação
        self.frame_delay = 10  #Tempo de atraso entre quadros de animação
        self.frame_counter = 0  #Contador para controlar o atraso
        self.walls = walls  
        self.rect = pygame.Rect(self.x, self.y, self.frame_width, self.frame_height)  # Retângulo do jogador para posição e colisão

    #Método para carregar quadros de animação da folha de sprites
    def load_frames(self):
        frames = []
        for row in range(self.rows):  
            direction_frames = []  
            for col in range(self.cols):
                # Calcula a posição e recorta o quadro da folha de sprites
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                direction_frames.append(frame)  #Adiciona o quadro à direção atual
            if direction_frames:
                frames.append(direction_frames)  # diciona os quadros da direção à lista principal
        return frames  #Retorna todos os quadros de animação

    #Método para atualizar a animação do jogador
    def update_animation(self):
        if self.direction < len(self.frames):  #Verifica se a direção tem quadros
            self.frame_index = self.frame_index % len(self.frames[self.direction])  #Atualiza o índice do quadro
            self.frame_counter += 1  #Incrementa o contador de atraso
            if self.frame_counter >= self.frame_delay:  #Verifica se o atraso foi atingido
                self.frame_counter = 0  #Reinicia o contador de atraso
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])  #Passa ao próximo quadro

    #Método para mover o jogador com base nas teclas pressionadas
    def move(self, keys):
        old_x, old_y = self.x, self.y  #Salva a posição atual do jogador

        #Move o jogador e define a direção com base nas teclas
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
            self.frame_index = 0  #Reseta o índice de quadro se nenhuma tecla de movimento é pressionada

        self.rect.topleft = (self.x, self.y)  #Atualiza a posição do retângulo do jogador

        #Verifica colisão com as paredes
        if any(self.rect.colliderect(wall) for wall in self.walls):
            self.x, self.y = old_x, old_y  #Reverte para a posição anterior se colidir
            self.rect.topleft = (self.x, self.y)  #Atualiza o retângulo

        #Se o jogador se moveu, atualiza a animação
        if any([keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP]]):
            self.update_animation()

    #Método para desenhar o jogador na tela
    def draw(self, surface, camera):
        #Verifica se a direção e o quadro atual são válidos
        if self.direction < len(self.frames) and self.frame_index < len(self.frames[self.direction]):
            frame_image = self.frames[self.direction][self.frame_index]  #Obtém o quadro atual
            #Desenha o quadro na tela, ajustado pela posição da câmera
            surface.blit(frame_image, camera.apply(self.rect))

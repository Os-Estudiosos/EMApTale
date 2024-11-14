import pygame
import os

from config import *

from classes.player import Player

from utils import sign


class Frisk(Player):
    """Gerencia o jogador, incluindo animação, movimento e colisões
    """
    def __init__(self, walls, *groups):
        super().__init__(*groups)

        self.scale_factor = 2.5  # Fator de escala para o jogador

        self.sprite_sheet = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'frisk.png')).convert_alpha(),  # Carrega a imagem do jogador
            self.scale_factor
        )
        self.frame_width = 24  # Largura de cada quadro de animação
        self.frame_height = 34  # Altura de cada quadro de animação

        self.cols = 2  # Número de colunas na folha de sprites
        self.rows = 4  # Número de linhas na folha de sprites

        self.frames = self.load_frames()

        self.x, self.y = 150, 350  # Posição inicial do jogador

        self.direction = 0  # Direção inicial do jogador

        self.frame_index = 0  # Índice do quadro atual de animação
        self.frame_delay = 10  # Tempo de atraso entre quadros de animação
        self.frame_counter = 0  # Contador para controlar o atraso

        self.walls = walls  # Lista de retângulos de colisão
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
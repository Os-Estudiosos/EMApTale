import pygame
import os

from config import *

from classes.player import Player
from classes.sprites.spritesheet import SpriteSheet
from classes.polygon.polygon import Polygon

from utils import sign


class Frisk(Player):
    """Gerencia o jogador, incluindo animação, movimento e colisões
    """
    def __init__(self, walls, *groups):
        super().__init__(*groups)

        self.scale_factor = 2.5  # Fator de escala para o jogador

        self.sprite_sheet = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'frisk.png')).convert_alpha()  # Carrega a imagem do jogador
        self.frame_width = 19  # Largura de cada quadro de animação
        self.frame_height = 29  # Altura de cada quadro de animação

        self.cols = 2  # Número de colunas na folha de sprites
        self.rows = 4  # Número de linhas na folha de sprites

        self.frame_offset = (3, 4)

        self.rect = pygame.Rect(150, 350, self.frame_width * self.scale_factor, self.frame_height * self.scale_factor)

        self.direction = 0  # Direção inicial do jogador

        self.frame_index = 0  # Índice do quadro atual de animação
        self.frame_delay = 10  # Tempo de atraso entre quadros de animação
        self.frame_counter = 0  # Contador para controlar o atraso

        self.walls = walls  # Lista de retângulos de colisão
        self.mask = None  # Máscara para colisão precisa

        self.frames = SpriteSheet(
            self.rows,
            self.cols,
            self.sprite_sheet,
            self.frame_width,
            self.frame_height,
            *self.frame_offset,
            self.scale_factor
        )

        self.speed = 7

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

    def move(self, camera, keys):
        direction = pygame.math.Vector2(
            sign((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) or (keys[pygame.K_d] - keys[pygame.K_a])),
            sign((keys[pygame.K_DOWN] - keys[pygame.K_UP]) or (keys[pygame.K_s] - keys[pygame.K_w]))
        )

        if direction.length() != 0:
            direction = direction.normalize()

        # Atualiza a direção e a animação
        self.update_dir(direction)
        if direction.length() != 0:
            self.update_animation()
        
        # Verifica colisão de máscara com as paredes
        # Movimenta o jogador
        self.rect.x += self.speed * direction.x

        wall = self.check_wall_collisions(camera, direction)
        if isinstance(wall, pygame.Rect):
            if direction.x > 0:
                self.rect.right = wall.left
            elif direction.x < 0:
                self.rect.left = wall.right
        if isinstance(wall, Polygon):
            self.rect.x -= self.speed * direction.x

        self.rect.y += self.speed * direction.y

        wall = self.check_wall_collisions(camera, direction)
        if isinstance(wall, pygame.Rect):
            if direction.y < 0:
                self.rect.top = wall.bottom
            elif direction.y > 0:
                self.rect.bottom = wall.top
        if isinstance(wall, Polygon):
            self.rect.y -= self.speed * direction.y

    def check_wall_collisions(self, camera, direction):
        """
        Verifica colisão de máscara entre o jogador e as paredes.
        """
        collided_wall = None
        for wall in self.walls:
            if wall.colliderect(self.rect):
                collided_wall = wall
            
        return collided_wall

    def draw(self, surface, camera):
        frame_image = self.frames[self.direction][self.frame_index]
        surface.blit(frame_image, camera.apply(self.rect))

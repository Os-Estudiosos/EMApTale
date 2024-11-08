import pygame
import os
import numpy as np
from config import GET_PROJECT_PATH
from utils import sign
import random

from classes.battle.container import BattleContainer
from classes.player import Player


class Heart(Player):
    def __init__(self, container: BattleContainer, *groups):
        """Inicialização da classe

        Args:
            container (BattleContainer): O Container da batalha, servirá para detecção da colisão
        """
        super().__init__(*groups)

        self.sprites: dict[str, pygame.Surface] = {
            'normal': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
                1.3
            ),
            'laugh': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'branco-heart.png')),
                1.3
            ),
            'inverse': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'yuri-heart.png')),
                1.3
            ),
            'confused': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'walter-heart.png')),
                1.3
            ),
            'prisioned': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'soledad-heart.png')),
                1.3
            ),
            'vanished': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'pinho-heart.png')),
                1.3
            )
        }

        self.image = self.sprites['normal']
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (
            pygame.display.get_window_size()[0]/2,
            pygame.display.get_window_size()[1]/2
        )
        
        self.container: BattleContainer = container
        self.effect = 'normal'
        self.speed = 5
        self.delay_time = 2000
        self.next_position_time = pygame.time.get_ticks() + self.delay_time
        self.circle_drawn = False
        self.next_x = self.rect.x
        self.next_y = self.rect.y
    
    def apply_effect(self, effect: str):
        self.image = self.sprites[effect]
        self.effect = effect
    
    def update(self, *args, **kwargs):
        keys = pygame.key.get_pressed()

        # Movimentação
        direction = pygame.math.Vector2(  # Faço um vetor que representa a direção que estou me movendo
            sign(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]),
            sign(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        )
        
        # Normalizo para andar sempre na mesma velocidade
        if direction.length() != 0:  
            direction = direction.normalize()

        # # Aplicando os efeitos 

        if self.effect == 'inverse':
            # Inverto as direções
            direction *=-1

        if self.effect == 'laugh':
            # Crio um vetor aleatório
            random_vector = np.random.uniform(-1, 1, 2)
            module = np.linalg.norm(random_vector)
            random_vector = random_vector/module
            # Mudo a direção causando uma pertubação
            direction.x += random_vector[0]*random.random()/2*self.speed
            direction.y += random_vector[1]*random.random()/2*self.speed
        
        if self.effect == 'vanished':
            # Apenas efeito visual
            pass
            
        if self.effect == 'confused':
            # Armazeno o tempo passado do jogo
            actual_time = pygame.time.get_ticks()
            # Se já passou o tempo para desenhar o círculo
            if actual_time >= self.next_position_time-500 and not self.circle_drawn:  # Desenha o círculo antes de mover
                # Calcula a próxima posição aleatória onde o personagem vai aparecer
                self.next_x = random.randint(
                    self.container.inner_rect.left + self.rect.width,
                    self.container.inner_rect.right - self.rect.width
                )
                self.next_y = random.randint(
                    self.container.inner_rect.top + self.rect.height,
                    self.container.inner_rect.bottom - self.rect.height
                )
                self.circle_drawn = True
            # Desenha o círculo na posição futura
            if self.circle_drawn and actual_time < self.next_position_time:
                pygame.draw.circle(
                    pygame.display.get_surface(),
                    (255, 165, 0),
                    (self.next_x + self.rect.width // 2, self.next_y + self.rect.height // 2),
                    5
                )
            # Verifica se é o momento de atualizar a posição do personagem
            if actual_time >= self.next_position_time:
                # Move o personagem para a próxima posição
                self.rect.x = self.next_x
                self.rect.y = self.next_y
                # Define o próximo tempo de atualização da posição
                self.next_position_time = actual_time + self.delay_time
                self.circle_drawn = False

        if self.effect == 'prisioned':
            lines = pygame.draw.lines(
                surface=pygame.display.get_surface(), 
                color=(255,255,255),
                points=[(self.container.inner_rect.centerx-100, self.container.inner_rect.centery),
                        (self.container.inner_rect.centerx+100, self.container.inner_rect.centery),
                        (self.container.inner_rect.centerx + 100, self.container.inner_rect.centery + 100),
                        (self.container.inner_rect.centerx + 100, self.container.inner_rect.centery)], 
                width=3,
                closed=False
                )

        # Mexendo na colisão
        # Esse código detecta se um ponto na frente do player está saindo do retangulo, se sair, eu paro de mexer o player
        if not self.container.out_rect.collidepoint(self.rect.centerx + (self.speed+self.mask.get_rect().width/2-7)*direction.x, self.rect.centery):
            direction.x = 0
        if not self.container.out_rect.collidepoint(self.rect.centerx, self.rect.centery + (self.speed+self.mask.get_rect().height/2-7)*direction.y):
            direction.y = 0

        # Mexo na posição
        self.rect.x += self.speed * direction.x
        self.rect.y += self.speed * direction.y

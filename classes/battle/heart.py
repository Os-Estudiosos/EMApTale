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

        # Definindo tudo que precisamos para movimentação e efeitos 
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
        self.direction = pygame.math.Vector2(0,0)
        self.delay_time = 2000
        self.next_position_time = pygame.time.get_ticks() + self.delay_time
        self.circle_drawn = False
        self.next_x = self.rect.x
        self.next_y = self.rect.y
        w = self.container.inner_rect.width
        h = self.container.inner_rect.height
        self.current_node = 'E'
        self.graph = {
            'A': {'pos': (w/1.3, h), 'neighbors': ['B', 'D']},
            'B': {'pos': (w, h), 'neighbors': ['A', 'C', 'E']},
            'C': {'pos': (1.25*w, h), 'neighbors': ['B', 'F']},
            'D': {'pos': (w/1.3, (h+1.8*h)/2), 'neighbors': ['A', 'E', 'G']},
            'E': {'pos': (w, (h+1.8*h)/2), 'neighbors': ['B', 'D', 'F', 'H']},
            'F': {'pos': (1.25*w, (h+1.8*h)/2), 'neighbors': ['C', 'E', 'I']},
            'G': {'pos': (w/1.3, 1.8*h), 'neighbors': ['D', 'H']},
            'H': {'pos': (w, 1.8*h), 'neighbors': ['E','G', 'I']},
            'I': {'pos': (1.25*w, 1.8*h), 'neighbors': ['F', 'H']}
        }
    
    def apply_effect(self, effect: str):

        # Aplicando o efeito no coração
        self.image = self.sprites[effect]
        self.effect = effect
    
    def apply_effect_inverse(self):

        # Inverto a direção
        self.direction *= -1
    
    def apply_effect_laugh(self):

        # Crio um vetor aleatório
        random_vector = np.random.uniform(-1, 1, 2)
        module = np.linalg.norm(random_vector)
        random_vector = random_vector/module

        # Mudo a direção causando uma pertubação
        self.direction.x += random_vector[0]*random.random()/2*self.speed
        self.direction.y += random_vector[1]*random.random()/2*self.speed
    
    def apply_effect_vanished(self):

        # Apenas efeito visual
        pass

    def apply_effect_confused(self):

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

    def draw_graph(self, graph:dict):

        # Desenhando o grafo e os nós
        for node, data in graph.items():
            for neighbor in data["neighbors"]:
                pygame.draw.line(
                    surface=pygame.display.get_surface(), 
                    color=(255,255,255),
                    start_pos=data["pos"],
                    end_pos=graph[neighbor]["pos"],
                    width=2)
        for node, data in graph.items():
            pygame.draw.circle(
                surface=pygame.display.get_surface(),
                color=(128,0,128),
                center=data["pos"],
                radius=7
            )

    def move_to_neighbor(self, direction):

        # Movimenta o personagem para um nó vizinho com base na direção
        neighbors = self.graph[self.current_node]['neighbors']
        
        # Mapeamento de teclas para os nós vizinhos
        if direction == 'right' and len(neighbors) > 1:
            self.current_node = neighbors[1]
            self.rect.center = self.graph[self.current_node]['pos']
        elif direction == 'left' and len(neighbors) > 0:
            self.current_node = neighbors[0]
            self.rect.center = self.graph[self.current_node]['pos']
        elif direction == 'down' and len(neighbors) > 2:
            self.current_node = neighbors[2]
            self.rect.center = self.graph[self.current_node]['pos']
        elif direction == 'up' and len(neighbors) > 3:
            self.current_node = neighbors[3]
            self.rect.center = self.graph[self.current_node]['pos']

    def apply_effect_prisioned(self):

        # Lógica da movimentação do personagem apenas nos nós
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.move_to_neighbor('right')
        elif keys[pygame.K_LEFT]:
            self.move_to_neighbor('left')
        elif keys[pygame.K_DOWN]:
            self.move_to_neighbor('down')
        elif keys[pygame.K_UP]:
            self.move_to_neighbor('up')

        # Defino a posição inicial do personagem
        self.rect.center = self.graph[self.current_node]['pos']

        # Desenho o grafo
        self.draw_graph(graph=self.graph)

    def update(self, *args, **kwargs):
        keys = pygame.key.get_pressed()

        # Movimentação
        self.direction = pygame.math.Vector2(  # Faço um vetor que representa a direção que estou me movendo
            sign(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]),
            sign(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        )
        
        # Normalizo para andar sempre na mesma velocidade
        if self.direction.length() != 0:  
            self.direction = self.direction.normalize()

        # # Aplicando os efeitos 

        if self.effect == 'inverse':
            self.apply_effect_inverse()
        if self.effect == 'laugh':
            self.apply_effect_laugh()
        if self.effect == 'vanished':
            self.apply_effect_vanished()
        if self.effect == 'confused':
            self.apply_effect_confused()
        if self.effect == 'prisioned':
            self.apply_effect_prisioned()

        # Mexendo na colisão
        # Esse código detecta se um ponto na frente do player está saindo do retangulo, se sair, eu paro de mexer o player
        if not self.container.out_rect.collidepoint(self.rect.centerx + (self.speed+self.mask.get_rect().width/2-7)*self.direction.x, self.rect.centery):
            self.direction.x = 0
        if not self.container.out_rect.collidepoint(self.rect.centerx, self.rect.centery + (self.speed+self.mask.get_rect().height/2-7)*self.direction.y):
            self.direction.y = 0

        # Mexo na posição
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y

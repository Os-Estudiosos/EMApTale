import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

class CoffeeCup(pygame.sprite.Sprite):
    def __init__(self, x, y, drops_group, *groups):
        """
        Representa uma xícara de café com gotas e vapor animados.
        """
        super().__init__(*groups)

        # Carregando o sprite da xícara
        self.image_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png')
        self.image = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(),
            (100, 100)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0  # Ângulo inicial
        self.flip_speed = 2  # Velocidade de giro
        self.flipping = False  # Flag para iniciar o giro
        self.drop_timer = 0  # Controle de tempo para criar gotas
        self.drop_interval = 5000  # Intervalo entre gotas
        self.gravity = 0.3
        self.counter = 0
        self.counter_rate = FPS*0.5
        self.drops_group = pygame.sprite.Group()
        CombatManager.global_groups.append(self.drops_group)


    def start_flip(self):
        """Inicia a animação de virar a xícara."""
        self.flipping = True
        self.angle = 0
        self.drop_timer = 0
        self.y_velocity = 1

    def update(self, *args, **kwargs):
        """Atualiza o estado da xícara e suas animações."""
        self.counter += 1
        # Animação de virar a xícara
        if self.flipping:
            if self.angle < 180:
                self.angle += self.flip_speed
            else:
                self.angle = 180
                self.flipping = False

            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(self.image_path).convert_alpha(),
                (100, 100)
            ), self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y += self.y_velocity

        # Controla a criação de gotas enquanto está girando
        if self.flipping and self.angle > 90:  # Começa a derramar gotas após meio-giro
            self.drop_timer += 1
            if self.drop_timer >= self.drop_interval:
                self.drop_timer = 0
                if random.random() < 0.3:  # 30% de chance
                    drop = CoffeeDrop(self.drops_group)
        
class CoffeeDrop(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Colocando uma chance de colocar o efeito
        self.type = 'Normal'
        if random.randint(0, 100) <= 15:
            self.type = 'Vanished'

        # Criando os sprites para gotas
        self.image_path = pygame.image.load(
            os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'drop_coffee.png')
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image_path, (50, 50))
        self.rect = self.image.get_rect()
        self.coffee_mask = pygame.mask.from_surface(self.image)
        
        # Velocidade da gota
        self.flip_speed = 0.5  # Velocidade aleatória para variação
        self.gravity = 0.05  # Aceleração para queda

        self.randomize_position()


    def randomize_position(self):
        """Define uma posição aleatória para as gotas."""

        battle_container = CombatManager.get_variable('battle_container')
        display_rect = battle_container.inner_rect
        self.rect.top = display_rect.top-50
        self.rect.x = random.randint(display_rect.width-8, 2*display_rect.width-35)

        self.rect.y += self.gravity

    def vanished(self):
        """
        Muda o sprite da gota quando aplicamos ela tem o efeito
        """
        if self.type == 'Vanished':
            self.image_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'water_drop.png')

    def draw_drops(self, surface):
        """
        Desenha as gotas associadas à xícara.

        Args:
            surface (pygame.Surface): Superfície onde os elementos serão desenhados.
        """
        self.drops_group.draw(surface)

    def update(self, *args, **kwargs):
        # Atualizar posição
        self.rect.y += self.flip_speed
        self.flip_speed += self.gravity  # Aplicar gravidade

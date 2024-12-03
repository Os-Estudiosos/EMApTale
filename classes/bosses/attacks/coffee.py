import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

class Coffee(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        """
        Representa uma xícara de café com gotas e vapor animados.
        """
        super().__init__(*groups)

        # Carregando o sprite da xícara
        self.image_path = pygame.image.load(
            os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png')
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image_path, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

    def start_flip(self):
        """Inicia a animação de virar a xícara."""
        self.flipping = True
        self.y_velocity = 2

    def update(self, *args, **kwargs):
        """Atualiza o estado da xícara e suas animações."""
        # Animação de virar a xícara
        if self.flipping:
            if self.angle < 180:
                self.angle += self.flip_speed
            else:
                self.angle = 180
                self.flipping = False

            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y += self.y_velocity

        # Controla a criação de gotas enquanto está girando
        if self.flipping and self.angle > 90:  # Começa a derramar gotas após meio-giro
            self.drop_timer += 1
            if self.drop_timer >= self.drop_interval:
                self.drop_timer = 0
                self.create_drop()

        self.rect.y += self.speed
        self.speed += self.gravity

        # Remove a gota se sair da tela e enche a tela de café
        display_rect = pygame.display.get_surface().get_rect()
        if self.rect.top > display_rect.height:
            self.kill()
            self.coffee_fill_rect_height +=1

            if self.coffee_fill_rect_height >= CombatManager.get_variable('battle_container').inner_rect.height - 80:
                self.coffee_fill_rect_height = CombatManager.get_variable('battle_container').inner_rect.height - 80


        # Atualiza grupos de animações
        self.drops_group.update()
        self.puddle_group.update()



class CoffeeDrop(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Colocando uma chance de colocar o efeito
        self.type = 'Normal'
        if random.randint(0, 100) <= 15:
            self.type = 'Vanished'

        # Criando os sprites para gotas
        self.coffee_image_path = pygame.image.load(
            os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'drop_coffee.png')
        ).convert_alpha()
        self.coffee_image = pygame.transform.scale(self.coffee_image_path, (50, 50))
        self.coffee_rect = self.coffee_image.get_rect()
        self.coffee_mask = pygame.mask.from_surface(self.coffee_image)
        self.randomize_position()
        
        # Grupos para animações adicionais
        self.drops_group = pygame.sprite.Group()

        # Animação de virar
        self.angle = 0
        self.flip_speed = 5
        self.flipping = False
        self.y_velocity = 0

        # Velocidade da gota
        self.speed = random.randint(5, 10)  # Velocidade aleatória para variação
        self.gravity = 0.5  # Aceleração para queda
        self.coffee_fill_rect_width = CombatManager.get_variable('battle_container').inner_rect.width
        self.coffee_fill_rect_height = 0

    def randomize_position(self):
        """Define uma posição aleatória para as gotas."""
        battle_container = CombatManager.get_variable('battle_container')
        display_rect = battle_container.inner_rect
        self.rect.top = random.randint(30, display_rect.width - 30)
        self.rect.y = random.randint(30, display_rect.height - 30)

        if self.rect.colliderect(battle_container.out_rect):
            self.rect.x += battle_container.out_rect.width * random.choice([1, -1])
            self.rect.y += battle_container.out_rect.height * random.choice([1, -1])

    def change_sprite(self):
        """
        Muda o sprite da gota quando aplicamos o efeito
        """
        if self.type == 'Vanished':
            self.coffee_image_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'water_drop.png')

    def draw_drops(self, surface):
        """
        Desenha as gotas associadas à xícara.

        Args:
            surface (pygame.Surface): Superfície onde os elementos serão desenhados.
        """
        self.drops_group.draw(surface)
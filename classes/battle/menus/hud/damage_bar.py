import pygame
import os
from random import choice
from config import *

from classes.battle.container import BattleContainer


class DamageBar(pygame.sprite.Sprite):
    """Classe da barrinha que indica o dano
    """
    def __init__(self, container: BattleContainer, groups: tuple[pygame.sprite.Group] = ()):
        super().__init__(*groups)

        self.sprites = [  # Lista com os sprites
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_bar_1.png')),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', 'damage_bar_2.png'))
        ]
        for i in range(len(self.sprites)):  # Redimensiono os sprites mas mantenho sua largura
            self.sprites[i] = pygame.transform.scale(
                self.sprites[i],
                (
                    self.sprites[i].get_width(),
                    pygame.display.get_surface().get_height()*0.3
                )
            )

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

        self.container = container  # O  Container preto que o menu fica

        self.random_dir = 0  # A direção onde minha barra vai se mexer
        self.speed = 10  # Velocidade da barra

        self.execution_counter = 0  # Contador de updates

        self.animation_counter = 0  # Contador da animação
        self.frame_changes_per_second = FPS/10  # Taxa de frames da animação por segundo
        self.actual_sprite = 0  # Sprite atual
    
    def change_sprite(self):
        """Método responsável por mudar o sprite
        """
        self.actual_sprite+=1  # Somo 1 ao sprite atual
        if self.actual_sprite >= len(self.sprites):  # Se o contador do sprite passar do len, eu zero
            self.actual_sprite = 0
        self.image = self.sprites[self.actual_sprite]  # Mudo o sprite
        self.animation_counter = 0  # Zero o contador da animação

    def choose_direction(self):
        """Método responsável por escolher a direção onde a barrinha fica se movendo
        """
        self.random_dir = choice([1, -1])  # Escolho uma 
        # Coloco a barra na posição correta
        self.rect.centerx = self.container.inner_rect.centerx + (self.container.inner_rect.width/2)*self.random_dir
        keys = pygame.key.get_pressed()

        # Como é o primeiro método que eu executo ao criar a barra, eu checo para garantir que o
        # Player não entrou na opção de lutar com o botão pressionado por acidente
        if keys[pygame.K_z] or keys[pygame.K_RETURN]:
            self.entered_pressing = True

    def update(self, *args, **kwargs):
        keys = pygame.key.get_pressed()

        # Se eu apertar o botão de ENTER ou Z
        if (keys[pygame.K_z] or keys[pygame.K_RETURN]) and not self.entered_pressing:
            self.random_dir = 0  # Paro de mover a barra
            self.entered_pressing = True

        if not keys[pygame.K_RETURN] and not keys[pygame.K_z]:
            self.entered_pressing = False
        
        self.animation_counter += 1  # Aumento o contador da animação
        # Se a barrinha estiver parada e o contador for maior que a taxa de frames por segundo
        if self.random_dir == 0 and self.animation_counter >= self.frame_changes_per_second:
            self.change_sprite()  # Mudo o sprite

        self.rect.x += self.speed*self.random_dir*-1  # Mexo a barra
        self.rect.centery = self.container.inner_rect.centery  # Centralizo a barra
import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager



class Coffee(pygame.sprite.Sprite):
    def __init__(self,*groups):
        """
        Representa uma xícara de café com vapor animado.
        
        Args:
            x (int): Coordenada x da posição inicial da xícara.
            y (int): Coordenada y da posição inicial da xícara.
            groups (pygame.sprite.Group): Grupos aos quais o sprite pertence.
        """
        super().__init__(*groups)

        # Carregando o sprite da xícara, da gota e da poça de café
        self.cup_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'cup_coffee.png')
        self.cup_image = pygame.transform.scale(pygame.image.load(self.cup_path), (100,100)).convert_alpha()
        self.drop_coffee_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'drop_coffee.png')
        self.drop_coffee_image = pygame.transform.scale(pygame.image.load(self.drop_coffee_path), (50,50)).convert_alpha()
        self.puddle_coffee_path = os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'drop_coffee.png')
        self.puddle_coffee_image = pygame.transform.scale(pygame.image.load(self.puddle_coffee_path), (50,50)).convert_alpha()
        
        self.coffee_group = pygame.sprite.Group().add([self.cup_image, self.drop_coffee_image, self.puddle_coffee_image])
        #CombatManager.enemy.rect
    def update(self, *args, **kwargs):
        """
        Atualiza o estado da xícara e anima o vapor.
        """
        # Atualiza a posição da fumaça para alinhar com a xícara
        self.smoke.rect.midbottom = self.rect.midtop

        # Atualiza a fumaça
        self.smoke_group.update()
        if pygame.sprite.spritecollide(self.player, self.coffee_group, True, pygame.sprite.collide_mask):
            self.player.take_damage(CombatManager.enemy.damage)

    def randomize_position(self):
        battle_container = CombatManager.get_variable('battle_container')  # Pego o container
        display_rect = pygame.display.get_surface().get_rect()  # Pego a superfície da tela
        self.rect.x = random.randint(30, display_rect.width-30)  # Gero aleatoriamente dentro da tela
        self.rect.y = random.randint(30, display_rect.height-30)
        
        if self.rect.colliderect(battle_container.out_rect):  # Para sempre surgir fora do container
            self.rect.x += battle_container.out_rect.width * random.choice([1, -1])
            self.rect.y += battle_container.out_rect.height * random.choice([1, -1])

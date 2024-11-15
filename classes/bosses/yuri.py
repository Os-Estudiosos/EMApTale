import pygame
import os
import random

from config import *
from config.eventmanager import EventManager
from config.combatmanager import CombatManager

from classes.bosses import Boss, Attack
from classes.battle.heart import Heart

from classes.bosses.attacks.vector import Vector

from constants import PLAYER_TURN_EVENT


class Yuri(Boss):
    name = 'Yuri Saporito'

    def __init__(self, infos: dict, *groups):
        """Inicialização da classe Yuri

        Args:
            infos (dict): Dicionário com as informações sobre o BOSS
            variables (dict): Variáveis extras que serão usadas na lógica do Boss
        """
        super().__init__(*groups)
        
        # Carregando o sprite do Yuri
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'yuri.png'))
        self.rect = self.image.get_rect()

        # Definindo os atributos
        self.__life = infos['life']
        self.__max_life = infos['life']
        self.__damage = infos['damage']
        self.__defense = infos['defense']
        self.__voice = infos['voice']

        # Lista dos ataques que ele vai fazer
        self.__attacks = [
            YuriAttack1()
        ]
        self.attack_to_execute = -1
    
    def speak(self, text):
        ...
    
    def choose_attack(self):
        self.attack_to_execute = random.randint(0, len(self.__attacks)-1)
        self.__attacks[self.attack_to_execute].restart()
        print(self.attack_to_execute)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, *args, **kwargs):
        self.rect.centerx = pygame.display.get_surface().get_width()/2

        if 0 <= self.attack_to_execute < len(self.__attacks):
            if self.__attacks[self.attack_to_execute].duration_counter >= self.__attacks[self.attack_to_execute].duration:
                self.attack_to_execute = -1
            else:
                self.__attacks[self.attack_to_execute].run()

    
    def take_damage(self, amount):
        self.__life -= amount

    @property
    def life(self):
        return self.__life
    
    @property
    def max_life(self):
        return self.__max_life

    @property
    def damage(self):
        return self.__damage
    
    @property
    def defense(self):
        return self.__defense
    
    @property
    def voice(self):
        return self.__voice


class YuriAttack1(Attack):
    def __init__(self):
        self.__player: Heart = CombatManager.get_variable('player')
        self.__player_group: pygame.sprite.Group = CombatManager.get_variable('player_group')

        self.vectors_group = pygame.sprite.Group()

        CombatManager.global_groups.append(self.vectors_group)

        self.vectors: list[Vector] = []
        self.vectors_creation_rate = FPS/3  # 3 Vetores a cada segundo serão criados

        self.duration = FPS * 10  # O Ataque dura 10 segundos
        self.duration_counter = 0

        # self.vectors.append(Vector(self.vectors_group))

    def run(self):
        self.duration_counter += 1

        if self.duration_counter % self.vectors_creation_rate == 0:
            self.vectors.append(Vector(self.vectors_group))
        
        if self.duration_counter >= self.duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            self.vectors_group.empty()
        
        for vector in self.vectors:
            vector.update(player_center=self.player.rect.center)
        
        for vector in self.vectors_group:
            if self.__player != vector:
                if self.__player.rect.colliderect(vector.rect):
                    offset = (vector.rect.x - self.__player.rect.x, vector.rect.y - self.__player.rect.y)
                    if self.__player.mask.overlap(vector.mask, offset):
                        self.__player.take_damage(CombatManager.enemy.damage)
                        vector.kill()
    
    def restart(self):
        self.duration_counter = 0
    
    @property
    def player(self):
        return self.__player

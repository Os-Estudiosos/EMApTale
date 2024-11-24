import pygame

from config import *
from config.combatmanager import CombatManager

from classes.bosses import Attack

from constants import *


class EmptyAttack(Attack):
    def __init__(self, damage):
        self.__player = CombatManager.get_variable('player')
        self.damage = damage

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

    def run(self):
        self.__duration_counter += 1
        
        if self.__duration_counter >= self.__duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
    
    def restart(self):
        self.__duration_counter = 0
    
    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter


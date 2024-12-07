import pygame

from config import *
from config.combatmanager import CombatManager


class NodeExplosion:
    def __init__(self, position: tuple[float], damage: float):
        self.warning_color = pygame.Color(255,0,0,100)
        self.boom_color = pygame.Color(255,255,255)
        self.position = position

        self.damage = damage

        self.player = CombatManager.get_variable('player')

        self.radius = 0
        self.max_radius = 20

        self.ray_growth_counter = 0
        self.ray_growth_rate = FPS/60

        self.transition_counter = 0
        self.transition_duration = FPS/2

        self.state = 'warning'

        self.warning_state_counter = 0

        self.boom_state_counter = 0
    
    def update(self):
        self.ray_growth_counter += 1

        if self.state == 'warning':
            if self.ray_growth_counter >= self.ray_growth_rate and self.radius <= self.max_radius:
                self.ray_growth_counter = 0
                self.radius += 1
            
            if self.radius >= self.max_radius:
                self.state = 'transition'
        elif self.state == 'transition':
            self.transition_counter += 1
            if self.transition_counter >= self.transition_duration:
                self.state = 'boom'
        elif self.state == 'boom':
            if self.radius >= 0:
                self.radius -= 2
            else:
                self.state = 'dead'
        
            if self.player.rect.center == self.position:
                self.player.take_damage(self.damage)
    
    def draw(self, screen: pygame.Surface):
        if self.state == 'warning' or self.state == 'transition':
            pygame.draw.circle(
                screen,
                self.warning_color,
                self.position,
                self.radius
            )
        if self.state == 'boom':
            pygame.draw.circle(
                screen,
                self.boom_color,
                self.position,
                self.radius
            )

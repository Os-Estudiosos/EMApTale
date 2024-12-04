import pygame
import random
import math

from config import *
from config.combatmanager import CombatManager

from classes.battle.heart import Heart

from utils import degrees_to_radians, line_between_two_points, distance_point_and_segment


class ClosingGraph:
    def __init__(self):
        self.nodes_amount = 8
        self.nodes = [[i, degrees_to_radians((360/self.nodes_amount)*i)] for i in range(self.nodes_amount)]
        self.edges = self.update_edges()

        self.container = CombatManager.get_variable('battle_container')
        self.player: Heart = CombatManager.get_variable('player')
        
        self.ray = 900

        self.ray_increment_speed = random.uniform(0.5,1)
        self.rotation_increment_speed = random.uniform(0.5,1)*random.choice([-1, 1])

        self.dead = False
    
    def check_player_collision(self):
        for edge in self.edges:
            point1 = (
                self.ray*math.cos(edge[0][1])+self.container.inner_rect.centerx,
                self.ray*math.sin(edge[0][1])+self.container.inner_rect.centery
            )
            point2 = (
                self.ray*math.cos(edge[1][1])+self.container.inner_rect.centerx,
                self.ray*math.sin(edge[1][1])+self.container.inner_rect.centery
            )

            line = line_between_two_points(
                point1,
                point2
            )

            distance_between_player_and_line = distance_point_and_segment(
                self.player.rect.centerx,
                self.player.rect.centery,
                point1[0],
                point1[1],
                point2[0],
                point2[1],
            )

            if (
                (distance_between_player_and_line <= 10)
                # and
                # (min(point1[0], point2[0]) <= self.player.rect.centerx <= max(point1[0], point2[0]))
            ):
                self.player.take_damage(5)
    
    def update_edges(self):
        return [[self.nodes[i], self.nodes[i+1], None] for i in range(self.nodes_amount-1)]

    def update(self):
        self.ray -= 5*self.ray_increment_speed
        if self.ray <= 0:
            self.dead = True
        
        self.check_player_collision()
        
        for i in range(self.nodes_amount):
            self.nodes[i][1] = (self.nodes[i][1] + degrees_to_radians(self.rotation_increment_speed))%(math.pi*2)
    
    def draw(self, screen):
        for edge in self.edges:  # Desenho as arestas
            pygame.draw.line(
                screen,
                (255,255,255),
                (
                    self.ray*math.cos(edge[0][1])+self.container.inner_rect.centerx,
                    self.ray*math.sin(edge[0][1])+self.container.inner_rect.centery
                ),
                (
                    self.ray*math.cos(edge[1][1])+self.container.inner_rect.centerx,
                    self.ray*math.sin(edge[1][1])+self.container.inner_rect.centery
                ),
                3
            )
        for node in self.nodes:  # Desenho os nós
            pygame.draw.circle(
                screen,
                (255,255,255),
                (
                    self.ray*math.cos(node[1])+self.container.inner_rect.centerx,
                    self.ray*math.sin(node[1])+self.container.inner_rect.centery
                ),
                5
            )

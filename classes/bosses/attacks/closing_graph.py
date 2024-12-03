import pygame
import networkx as nx
import math

from config import *
from config.combatmanager import CombatManager

from utils import degrees_to_radians


class ClosingGraph:
    def __init__(self):
        self.nodes_amount = 10
        self.nodes = [(i, degrees_to_radians((360/self.nodes_amount)*i)) for i in range(self.nodes_amount)]
        self.edges = [(self.nodes[i], self.nodes[i+1]) for i in range(self.nodes_amount-1)]

        self.actual_rotation = 0

        self.container = CombatManager.get_variable('battle_container')
        
        self.ray = 900

        self.dead = False

    def update(self):
        self.ray -= 5
        if self.ray <= 0:
            self.dead = True
    
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
                2
            )
        for node in self.nodes:  # Desenho os nós
            pygame.draw.circle(
                screen,
                (255,255,255),
                (
                    self.ray*math.cos(node[1])+self.container.inner_rect.centerx,
                    self.ray*math.sin(node[1])+self.container.inner_rect.centery
                ),
                3
            )

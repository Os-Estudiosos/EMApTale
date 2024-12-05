import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

import pygame
import os
import random

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

class Histogram(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Inicializando as infos para as barras
        self.min_height = 0
        self.max_height = CombatManager.get_variable('battle_container').out_rect.height+50
        self.start_pos = 10
        self.num_rects = 10
        self.rects_color = (15, 158, 213)
        self.rects = []
        self.speeds = []

        self.on_attack = False

        # Inicializando os grupos
        self.bars_group = pygame.sprite.Group()
        self.axis_group = pygame.sprite.Group()
        CombatManager.global_draw_functions.append(self.draw_bars)

        self.counter = 0

    def update(self, *args, **kwargs):
        """Atualiza as barras, alterando suas alturas dinamicamente."""
        if self.counter == 0:
            # Gerar retângulos
            self.randomize_bars()
        self.counter += 1
        for i, rect in enumerate(self.rects):
            rect.height += self.speeds[i]

            # Inverter direção ao atingir limites
            if rect.height >= self.max_height or rect.height <= self.min_height:
                self.speeds[i] = -self.speeds[i]
            
            rect.bottom = CombatManager.get_variable('battle_container').inner_rect.bottom

    def randomize_bars(self):
        """Gera barras com alturas e velocidades aleatórias."""
        battle_container = CombatManager.get_variable('battle_container').inner_rect
        bar_width = CombatManager.get_variable('battle_container').inner_rect.width // self.num_rects
        self.rects = []
        self.speeds = []

        for i in range(self.num_rects):
            height = 10
            x = battle_container.x + i * bar_width
            rect = pygame.Rect(x, 0, bar_width - 5, height)  # Pequeno espaço entre as barras
            rect.top = battle_container.bottom
            self.rects.append(rect)
            self.speeds.append(random.randint(1, 5))  # Velocidades aleatórias

    def draw_bars(self, *args, **kwargs):
        """Desenha as barras na tela."""
        if self.on_attack:
            for rect in self.rects:
                pygame.draw.rect(pygame.display.get_surface(), self.rects_color, rect)
    
    def restart(self):
        self.counter = 0

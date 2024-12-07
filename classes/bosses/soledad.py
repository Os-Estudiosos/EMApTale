import pygame
import os
import random
import math
import networkx as nx

from config import *
from config.eventmanager import EventManager
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager
from config.fontmanager import FontManager

from classes.bosses import Boss, Attack
from classes.battle.heart import Heart
from classes.bosses.hp import BossHP

from classes.bosses.attacks.closing_graph import ClosingGraph
from classes.bosses.attacks.node_explosion import NodeExplosion

from classes.bosses.attacks.empty_attack import EmptyAttack

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion

from constants import PLAYER_TURN_EVENT, BOSS_TURN_EVENT, BOSS_ACT_EFFECT

from utils import degrees_to_radians


class Soledad(Boss):
    name = 'Soledad'

    def __init__(self, infos: dict, *groups):
        """Inicialização da classe Yuri

        Args:
            infos (dict): Dicionário com as informações sobre o BOSS
            variables (dict): Variáveis extras que serão usadas na lógica do Boss
        """
        super().__init__(*groups)
        
        # Carregando o sprite do Yuri
        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'soledad.png')),
            0.5
        )
        self.rect = self.image.get_rect()
        self.__state = 'idle'
        self.__counter = 0

        # Definindo os atributos
        self.__life = infos['life']
        self.__max_life = infos['life']
        self.__damage = infos['damage']
        self.__defense = infos['defense']
        self.__voice = infos['voice']
        self.__music = infos['sound']

        self.__attacks_dialogues = infos['attacks_dialogues']

        # Container que vai mostrar quando o Professor tomar dano
        self.hp_container = BossHP()

        # Lista dos ataques que ele vai fazer
        self.__attacks = [
            GraphClosingAttack(self.__damage),
            AttachedToGraph(self.__damage)
        ]
        self.attack_to_execute = -1

        self.dialogue = DialogueBox(
            '',
            FontManager.fonts['Gamer'],
            15,
            30,
            self.voice
        )
        self.speaking = False

        self.__dead = False
        self.__death_animation_counter = 0
        self.__death_explosions: list[Explosion] = []
        self.death_loops_counter = 255

    def speak(self):
        if not self.__dead:
            self.dialogue.text = self.__attacks_dialogues[random.randint(0, len(self.__attacks_dialogues)-1)]
            self.speaking = True
    
    def death_animation(self):
        self.__death_animation_counter += 1
        if self.__death_animation_counter >= FPS*0.3:
            self.death_loops_counter += 1
            self.__death_animation_counter = 0
            self.__death_explosions.append(Explosion('blue', position=(
                random.randint(self.rect.x, self.rect.x+self.rect.width),
                random.randint(self.rect.y, self.rect.y+self.rect.height)
            )))
        
        for i, explosion in enumerate(self.__death_explosions):
            explosion.update()
            if explosion.finished:
                del self.__death_explosions[i]
    
    def choose_attack(self):
        self.attack_to_execute = random.randint(0, len(self.__attacks)-1)
        self.__attacks[self.attack_to_execute].restart()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.__state == 'shaking':
            self.hp_container.draw(screen)
        if self.speaking:
            self.dialogue.draw(screen)

        for explosion in self.__death_explosions:
            screen.blit(explosion.img, explosion.rect)
    
    def update(self, *args, **kwargs):
        self.rect.centerx = pygame.display.get_surface().get_width()/2

        if self.__state == 'shaking':
            self.__counter += 10
            counter_in_radians = self.__counter*math.pi/180
            wave_factor = (math.cos(counter_in_radians)-1)/counter_in_radians
            self.rect.x += 40 * wave_factor
            self.hp_container.update(actual_life=self.__life, max_life=self.__max_life)
            if self.__counter >= FPS*1.5*10:
                self.__state = 'idle'
                self.__counter = 0
                pygame.event.post(pygame.event.Event(BOSS_TURN_EVENT))
        
        if not self.__dead:
            if self.speaking:
                self.dialogue.update()
                self.dialogue.rect.left = self.rect.right

                for event in EventManager.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                            if not self.dialogue.finished:
                                self.dialogue.skip()
                            else:
                                self.speaking = False

            if 0 <= self.attack_to_execute < len(self.__attacks) and not self.speaking:
                if self.__attacks[self.attack_to_execute].duration_counter >= self.__attacks[self.attack_to_execute].duration:
                    self.attack_to_execute = -1
                else:
                    self.__attacks[self.attack_to_execute].run()
        else:
            self.death_animation()
        
        for event in EventManager.events:
            if event.type == BOSS_ACT_EFFECT:
                self.apply_effect(event.effect)

    @property
    def attacks(self):
        return self.__attacks

    @property
    def counter(self):
        return self.__counter

    @property
    def state(self):
        return self.__state

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

    @property
    def music(self):
        return self.__music
    
    @property
    def dead(self):
        return self.__dead
    
    @life.setter
    def life(self, value):
        self.__life = value
    
    @max_life.setter
    def max_life(self, value):
        self.__max_life = value

    @damage.setter
    def damage(self, value):
        self.__damage = value
    
    @defense.setter
    def defense(self, value):
        self.__defense = value
    
    @voice.setter
    def voice(self, value):
        self.__voice = value

    @music.setter
    def music(self, value):
        self.__music = value
    
    @dead.setter
    def dead(self, value):
        self.__dead = value
    
    @state.setter
    def state(self, value):
        self.__state = value
    
    @counter.setter
    def counter(self, value):
        self.__counter = value


class GraphClosingAttack(Attack):
    def __init__(self, damage):
        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.display = pygame.display.get_surface()

        self.graph_creation_counter = 0
        self.graph_creation_rate = FPS*1.5

        self.graphs_list: list[ClosingGraph] = []

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

        CombatManager.global_draw_functions.append(self.draw_graphs)
    
    def create_graph(self):
        graph = ClosingGraph()
        return graph

    def draw_graphs(self, *args, **kwargs):
        for graph in self.graphs_list:
            graph.draw(self.display)

    def run(self):
        self.__duration_counter += 1
        self.graph_creation_counter += 1

        for i, graph in enumerate(self.graphs_list):
            if graph.dead:
                self.graphs_list.pop(i)
            else:
                graph.update()

        if self.graph_creation_counter >= self.graph_creation_rate:
            self.graphs_list.append(self.create_graph())
            self.graph_creation_counter = 0
        
        if self.__duration_counter >= self.__duration:
            self.graphs_list.clear()
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
    
    def restart(self):
        self.__duration_counter = 0
        self.graphs_list.clear()
    
    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter


class AttachedToGraph(Attack):
    def __init__(self, damage):
        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.display = pygame.display.get_surface()
        self.container = CombatManager.get_variable('battle_container')

        self.helper_surface = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)

        self.explosion_creation_counter = 0
        self.explosion_creation_rate = FPS/2

        self.player_graph = self.__player.graph

        self.explosions: list[NodeExplosion] = []

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

        CombatManager.global_draw_functions.append(self.draw)
    
    def draw(self, *args, **kwargs):
        self.display.blit(self.helper_surface, self.helper_surface.get_rect())
        self.helper_surface.fill((0,0,0,0))

        for node_explosion in self.explosions:
            node_explosion.draw(self.helper_surface)

    def run(self):
        if self.__duration_counter == 0:
            self.__player.apply_effect('prisioned')

        self.explosion_creation_counter += 1

        if self.explosion_creation_counter >= self.explosion_creation_rate:
            self.explosion_creation_counter = 0
            random_node = random.choice([
                'A','B','C','D','E','F','G','H','I'
            ])
            self.explosions.append(NodeExplosion(
                self.player_graph[random_node]['pos'],
                self.damage
            ))

            random_node = random.choice([
                'A','B','C','D','E','F','G','H','I'
            ])
            self.explosions.append(NodeExplosion(
                self.player_graph[random_node]['pos'],
                self.damage
            ))
        
        for node_explosion in self.explosions:
            node_explosion.update()

        self.__duration_counter += 1
        
        if self.__duration_counter >= self.__duration:
            self.explosions.clear()
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
    
    def restart(self):
        self.__duration_counter = 0
        self.explosions.clear()
    
    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter

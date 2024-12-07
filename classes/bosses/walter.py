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

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion
from classes.bosses.attacks.dices import Dice
from classes.bosses.attacks.histogram import Histogram

from constants import PLAYER_TURN_EVENT, BOSS_TURN_EVENT, BOSS_ACT_EFFECT


class Walter(Boss):
    name = 'Walter Sande'

    def __init__(self, infos: dict, *groups):
        """Inicialização da classe Yuri

        Args:
            infos (dict): Dicionário com as informações sobre o BOSS
            variables (dict): Variáveis extras que serão usadas na lógica do Boss
        """
        super().__init__(*groups)
        
        # Carregando o sprite do Yuri
        self.image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'walter.png')),
            1
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
            HistogramAttack(self.__damage),
            # DicesAttack(self.__damage)
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
    
    @property
    def music(self):
        return self.__music
    
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

class HistogramAttack(Attack):
    def __init__(self, damage):
        super().__init__()  # Garantir inicialização da classe base, se necessário

        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.display = pygame.display.get_surface()

        self.__duration = FPS * 10  # O ataque dura 10 segundos
        self.__duration_counter = 0

        # Configuração do histograma
        self.histogram = Histogram()  # Instância da classe Histogram
        self.histogram.randomize_bars()  # Inicializa as barras aleatoriamente

    def run(self):
        """Executa o ataque com duração controlada e animação de histograma."""
        if self.__duration_counter == 0:
            self.histogram.on_attack = True
        self.__duration_counter += 1

        # Atualizar o histograma
        self.histogram.update()

        # Verificar colisões entre o jogador e as barras
        for rect in self.histogram.rects:
            if rect.width >= 0 and rect.height >= 0:
                rect_surface = pygame.Surface(rect.size)
                rect_mask = pygame.mask.from_surface(rect_surface)
                offset = (rect.x-self.__player.rect.x, rect.y-self.__player.rect.y)

                if self.__player.mask.overlap(rect_mask, offset):  # Colisão com a barra
                    SoundManager.play_sound("arrow.wav")
                    self.__player.take_damage(self.damage)  # Aplicar dano ao jogador

        # Verificar se o tempo do ataque acabou
        if self.__duration_counter >= self.__duration:
            self.histogram.on_attack = False
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))  # Evento para mudar o turno do jogador

    def restart(self):
        """Reinicia o ataque, resetando o contador de duração."""
        self.__duration_counter = 0
        self.histogram.rects.clear()
        self.histogram.restart()

    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter


class DicesAttack(Attack):
    def __init__(self, damage):
        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.display = pygame.display.get_surface()
        self.container = CombatManager.get_variable('battle_container')

        self.dice_creation_counter = 0
        self.dice_creation_rate = FPS

        self.player_graph = self.__player.graph

        self.dices_group = pygame.sprite.Group()

        self.dices: list = []

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

        CombatManager.global_groups.append(self.dices_group)

    def run(self):
        if self.dice_creation_counter == 0:
            self.player.apply_effect('confused')
        self.dice_creation_counter += 1

        if self.dice_creation_counter >= self.dice_creation_rate:
            self.dice_creation_counter = 0
            self.dices.append(Dice(self.dices_group))
            self.dices.append(Dice(self.dices_group))

        
        for dice in self.dices:
            dice.update()

        self.__duration_counter += 1

        if pygame.sprite.spritecollide(self.player, self.dices_group, True, pygame.sprite.collide_mask):
            self.player.take_damage(self.damage)
        
        if self.__duration_counter >= self.__duration:
            self.dices.clear()
            self.dices_group.empty()
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
    
    def restart(self):
        self.__duration_counter = 0
        self.dices.clear()
        self.dices_group.empty()
    
    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter

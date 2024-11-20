import pygame
import os
import random
import math

from config import *
from config.eventmanager import EventManager
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager
from config.fontmanager import FontManager

from classes.bosses import Boss, Attack
from classes.battle.heart import Heart
from classes.bosses.hp import BossHP

from classes.bosses.attacks.vector import Vector

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion

from constants import PLAYER_TURN_EVENT, BOSS_TURN_EVENT, BOSS_ACT_EFFECT


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
        self.state = 'idle'
        self.counter = 0

        # Definindo os atributos
        self.__life = infos['life']
        self.__max_life = infos['life']
        self.__damage = infos['damage']
        self.__defense = infos['defense']
        self.__voice = infos['voice']

        self.__attacks_dialogues = infos['attacks_dialogues']

        # Container que vai mostrar quando o Professor tomar dano
        self.hp_container = BossHP()

        # Lista dos ataques que ele vai fazer
        self.__attacks = [
            VectorAttack()
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

        self.dead = False
        self.__death_animation_counter = 0
        self.__death_explosions: list[Explosion] = []
        self.death_loops_counter = 255
    
    def speak(self):
        if not self.dead:
            self.dialogue.text = self.__attacks_dialogues[random.randint(0, len(self.__attacks_dialogues)-1)]
            self.speaking = True
    
    def death_animation(self):
        self.__death_animation_counter += 1
        if self.__death_animation_counter >= FPS*0.3:
            self.death_loops_counter += 1
            self.__death_animation_counter = 0
            self.__death_explosions.append(Explosion('yellow', position=(
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
        if self.state == 'shaking':
            self.hp_container.draw(screen)
        if self.speaking:
            self.dialogue.draw(screen)

        for explosion in self.__death_explosions:
            screen.blit(explosion.img, explosion.rect)

    def apply_effect(self, effect):
        if effect == '-defense':
            self.__defense = 0
    
    def update(self, *args, **kwargs):
        self.rect.centerx = pygame.display.get_surface().get_width()/2

        if not self.dead:
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
        
        if self.state == 'shaking':
            self.counter += 10
            counter_in_radians = self.counter*math.pi/180
            wave_factor = (math.cos(counter_in_radians)-1)/counter_in_radians
            self.rect.x += 40 * wave_factor
            self.hp_container.update(actual_life=self.__life, max_life=self.__max_life)
            if self.counter >= FPS*1.5*10:
                self.state = 'idle'
                self.counter = 0
                pygame.event.post(pygame.event.Event(BOSS_TURN_EVENT))

    
    def take_damage(self, amount):
        self.__life = self.__life - amount*amount/(amount+self.__defense)
        SoundManager.play_sound('damage.wav')
        if self.__life <= 0:
            self.__life = 0
            self.dead = True
        self.state = 'shaking'
        self.counter = 0

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


class VectorAttack(Attack):
    def __init__(self):
        self.__player: Heart = CombatManager.get_variable('player')

        self.vectors_group = pygame.sprite.Group()

        CombatManager.global_groups.append(self.vectors_group)

        self.vectors: list[Vector] = []
        self.vectors_creation_rate = FPS/5  # 3 Vetores a cada segundo serão criados

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

        # self.vectors.append(Vector(self.vectors_group))

    def run(self):
        self.__duration_counter += 1

        if self.__duration_counter % self.vectors_creation_rate == 0:
            self.vectors.append(Vector(self.vectors_group))
        
        if self.__duration_counter >= self.__duration:
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
                        if vector.type == 'Inverted':
                            self.__player.apply_effect('inverse')
                        vector.kill()
    
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

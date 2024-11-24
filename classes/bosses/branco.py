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

from classes.bosses.attacks.laugh import Laugh
from classes.bosses.attacks.empty_attack import EmptyAttack

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion

from constants import PLAYER_TURN_EVENT, BOSS_TURN_EVENT, BOSS_ACT_EFFECT


class Branco(Boss):
    name = 'Branco'

    def __init__(self, infos: dict, *groups):
        """Inicialização da classe Yuri

        Args:
            infos (dict): Dicionário com as informações sobre o BOSS
            variables (dict): Variáveis extras que serão usadas na lógica do Boss
        """
        super().__init__(*groups)
        
        # Carregando o sprite do Yuri
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'branco.png'))
        self.rect = self.image.get_rect()
        self.state = 'idle'
        self.counter = 0

        self.laughing = False
        self.laugh_counter = 0
        self.laugh_random_counter = 0
        self.laugh_animation_counter = 0
        self.laugh_rate = FPS
        self.laugh_group = pygame.sprite.Group()
        self.laughs_list: list[Laugh] = []

        CombatManager.global_groups.append(self.laugh_group)

        self.player: Heart = CombatManager.get_variable('player')

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
            EmptyAttack(0)
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
            self.__death_explosions.append(Explosion('red', position=(
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
                    self.laughs_list.clear()
                    self.laugh_group.empty()
                    self.laugh_animation_counter = 0
                    self.laughing = False
                else:
                    self.__attacks[self.attack_to_execute].run()
                    self.randomize_laugh()
                    if self.laughing:
                        self.laugh()
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
    
    def randomize_laugh(self):
        self.laugh_random_counter += 1  # Atualizando o contador da risada

        if not self.laughing and self.laugh_random_counter >= self.laugh_rate:
            self.laugh_random_counter = 0
            random_change_of_laugh = random.randint(0, 100)

            if random_change_of_laugh <= 10:
                self.laughing = True

    def laugh(self):
        self.laugh_counter += 1
        self.laugh_animation_counter += 1

        counter_in_radians = self.laugh_animation_counter*math.pi/180
        wave_factor = math.sin(10*counter_in_radians)
        self.rect.y += 1 * wave_factor

        for laugh in self.laughs_list:
            laugh.update()
            offset = (laugh.rect.x - self.player.rect.x, laugh.rect.y - self.player.rect.y)

            if self.player.mask.overlap(laugh.mask, offset):
                self.player.apply_effect('laugh')

        if self.laugh_counter >= self.laugh_rate:
            self.laughs_list.append(Laugh(self, self.laugh_group))
            self.laugh_counter = 0

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

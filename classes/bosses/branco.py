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
from classes.bosses.attacks.integral import Integral
from classes.bosses.attacks.integral_sword import IntegralSword

from classes.bosses.attacks.empty_attack import EmptyAttack

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion
from classes.effects.eye_flash import EyeFlash

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
        self.__state = 'idle'
        self.__counter = 0

        self.integral_sword = IntegralSword(60)

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
        self.__music = infos['sound']

        self.__attacks_dialogues = infos['attacks_dialogues']

        # Container que vai mostrar quando o Professor tomar dano
        self.hp_container = BossHP()
        
        self.can_laugh = True

        # Lista dos ataques que ele vai fazer
        self.__attacks = [
            IntegralsAttack(self.__damage),
            IntegralSwordAttack(self.__damage, self.integral_sword, self)
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
    
    def show_black(self):
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'preto.png'))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def show_white(self):
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'branco.png'))
        self.rect = self.image.get_rect(center=self.rect.center)

    def speak(self):
        if not self.__dead:
            self.dialogue.text = self.__attacks_dialogues[random.randint(0, len(self.__attacks_dialogues)-1)]
            self.speaking = True

    def restart_attacks(self):
        super().restart_attacks()
        self.laughs_list.clear()
        self.laugh_group.empty()
    
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
        self.integral_sword.draw(screen)
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
            self.integral_sword.rect.centerx = self.rect.centerx
            self.integral_sword.rect.centery = self.rect.centery + 10

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
                    self.laughs_list.clear()
                    self.laugh_group.empty()
                    self.laugh_animation_counter = 0
                    self.laughing = False
                    self.integral_sword.rotate_image_to(60)
                else:
                    self.__attacks[self.attack_to_execute].run()
                    if self.can_laugh:
                        self.randomize_laugh()
                    if self.laughing:
                        self.laugh()
        else:
            self.death_animation()
        
        if self.attack_to_execute == -1:
            self.integral_sword.rect.centerx = self.rect.centerx
            self.integral_sword.rect.centery = self.rect.centery + 10
        
        for event in EventManager.events:
            if event.type == BOSS_ACT_EFFECT:
                self.apply_effect(event.effect)
    
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


class IntegralsAttack(Attack):
    def __init__(self, damage):
        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.integral_group = pygame.sprite.Group()
        self.integral_creation_counter = 0
        self.integral_creation_rate = FPS*0.8
        self.integral_list: list[Integral] = []

        CombatManager.global_groups.append(self.integral_group)

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

    def run(self):
        self.__duration_counter += 1
        self.integral_creation_counter += 1

        for integral in self.integral_list:
            integral.update()

            offset = (integral.rect.x - self.__player.rect.x, integral.rect.y - self.__player.rect.y)

            if self.__player.mask.overlap(integral.mask, offset):
                self.__player.take_damage(self.damage)

        if self.integral_creation_counter >= self.integral_creation_rate:
            self.integral_creation_counter = 0
            self.integral_list.append(Integral(1, 90, self.integral_group))
            self.integral_list.append(Integral(-1, 90, self.integral_group))
        
        if self.__duration_counter >= self.__duration:
            self.integral_list.clear()
            self.integral_group.empty()
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
    
    def restart(self):
        self.integral_list.clear()
        self.integral_group.empty()
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


class IntegralSwordAttack(Attack):
    def __init__(self, damage, integral_sword: IntegralSword, boss: Branco):
        self.__player: Heart = CombatManager.get_variable('player')
        self.damage = damage

        self.integral_sword = integral_sword
        self.boss = boss

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

        # Lista com os flashes dos olhos
        self.eye_flashes: list[EyeFlash] = []

        self.display = pygame.display.get_surface()

        self.eye_flashes_amount = 5

        self.showing_attacks = True
        self.attacking = False

        self.eye_flashes_group = pygame.sprite.Group()
        self.eye_flashes_counter = 0
        self.eye_flashes_rate = FPS/2
        self.cuts_types = []

        self.transition_time = 0
        self.transition_duration = FPS/2

        self.cutting_transition_counter = 0
        self.cutting_transition_duration = FPS/2
        self.wich_cut = 0

        CombatManager.global_groups.append(self.eye_flashes_group)

    def run(self):
        if self.__duration_counter == 0:
            self.boss.can_laugh = False

        self.__duration_counter += 1
        self.eye_flashes_counter += 1

        if self.showing_attacks:
            if self.eye_flashes_counter >= self.eye_flashes_rate and len(self.eye_flashes) < self.eye_flashes_amount:
                self.eye_flashes_counter = 0
                self.eye_flashes.append(EyeFlash(
                    random.choice([1, -1]),
                    random.choice([
                        'stop',
                        'movement'
                    ]),
                    self.eye_flashes_group
                ))
                self.cuts_types = [eye.type for eye in self.eye_flashes]

            self.boss.show_black()
        
            for eye_flash in self.eye_flashes:
                eye_flash.update()
                eye_flash.rect.center = self.boss.rect.center
                eye_flash.rect.centery -= 60
                eye_flash.rect.centerx += eye_flash.rect.width//2*eye_flash.dir
            
            if len(self.eye_flashes) == self.eye_flashes_amount and all([(not ef.animating) for ef in self.eye_flashes]):
                self.showing_attacks = False
        else:
            self.transition_time += 1
            
            if self.transition_time >= self.transition_duration:
                self.transition_time = self.transition_duration
                self.attacking = True
            
            if self.attacking:
                self.boss.show_white()
                self.integral_sword.rotate_image_to(-90)
                self.integral_sword.rect.centery = self.boss.rect.centery + 10
                
                # self.integral_sword.go_to((self.boss.rect.right+self.boss.rect.width//2, self.boss.rect.centery + 10))

                if not self.integral_sword.moving:
                    self.cutting_transition_counter += 1
                    self.integral_sword.update()
                    if self.cutting_transition_counter >= self.cutting_transition_duration:
                        self.cutting_transition_counter = 0
                        self.integral_sword.cut(self.cuts_types[self.wich_cut%len(self.cuts_types)])
                        self.wich_cut += 1

        if self.__duration_counter >= self.__duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            self.boss.can_laugh = True
    
    def restart(self):
        self.__duration_counter = 0
        self.boss.can_laugh = False
        self.cuts_types.clear()
        self.integral_sword.cuts_list.clear()
        self.eye_flashes_group.empty()
        self.showing_attacks = True
        self.attacking = False
        self.transition_time = 0
        self.eye_flashes_counter = 0
        self.eye_flashes.clear()
        self.wich_cut = 0
        self.boss.can_laugh = True
        self.integral_sword.restart()
    
    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration
    
    @property
    def duration_counter(self):
        return self.__duration_counter

import pygame
import os
import random
import math

import pygame.draw_py

from config import *
from config.eventmanager import EventManager
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager
from config.fontmanager import FontManager

from classes.bosses import Boss, Attack
from classes.battle.heart import Heart
from classes.bosses.hp import BossHP

from classes.bosses.attacks.snake import Snake
from classes.bosses.attacks.coffee import Coffee

from classes.text.dialogue_box import DialogueBox

from classes.effects.explosion import Explosion

from constants import PLAYER_TURN_EVENT, BOSS_TURN_EVENT, BOSS_ACT_EFFECT

'''DIVIDIR EM EVENTOS PARA FAZER A XÍCARA DE CAFÉ'''
class Pinho(Boss):
    name = 'Rafael Pinho'

    def __init__(self, infos:dict, *groups):
        super().__init__(*groups)

        # Carregando o sprite do Pinho
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'bosses', 'pinho.png'))
        self.rect = self.image.get_rect()
        self.state = 'idle'
        self.counter = 0

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
            #PythonAtatack(),
            CoffeeAttack()
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
        self.moment = 0

    def speak(self):
        """
        Função que faz a fala do boss
        """
        if not self.dead:
            self.dialogue.text = self.__attacks_dialogues[random.randint(0, len(self.__attacks_dialogues)-1)]
            self.speaking = True
    
    def death_animation(self):
        """
        Função que faz a animação de morte do boss
        """
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
        """
        Função que deixa os ataques em ordem aleatória
        """
        self.attack_to_execute = random.randint(0, len(self.__attacks)-1)
        self.__attacks[self.attack_to_execute].restart()
    
    def draw(self, screen:pygame.surface):
        """
        Função que desenha tudo na tela

        Args:
            screen (pygame.surface): Superfícei da tela que receberá o desenho
        """
        screen.blit(self.image, self.rect)
        if self.state == 'shaking':
            self.hp_container.draw(screen)
        if self.speaking:
            self.dialogue.draw(screen)

        for explosion in self.__death_explosions:
            screen.blit(explosion.img, explosion.rect)

    def apply_effect(self, effect:str):
        """
        Função que aplica o efeito no boss

        Args:
            effect (str): Efeito específico do boss
        """
        if effect == '-defense':
            self.__defense = 0
    
    def update(self, *args, **kwargs):
        """
        Função que atualiza os eventos e os turnos
        """
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

    
    def take_damage(self, amount:float):
        """
        Função que computa o dano no boss

        Args:
            amount (float): Valor do dano numa distribuição 
        """

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
    
    @property
    def music(self):
        return self.__music


class CoffeeAttack(Attack):
    def __init__(self):
        """
        Inicializa o ataque de café com xícaras e gotas sincronizados.
        """
        super().__init__()
        self._player: Heart = CombatManager.get_variable('player')
        self._duration = FPS * 10  # O ataque dura 10 segundos
        self._duration_counter = 0
        self.cups_created = False

        # Configurações das xícaras
        battle_container = CombatManager.get_variable('battle_container')
        self.screen_width = battle_container.inner_rect.width
        self.screen_height = battle_container.inner_rect.height

        self._cup = pygame.sprite.Group()
        self._drops = pygame.sprite.Group()

    def run(self):
        """
        Executa o ataque, atualizando as xícaras e verificando colisões.
        """
        # Criando xícaras
        if not self.cups_created:
            coffee_cup = Coffee(x=CombatManager.enemy.rect.midleft[0], y=CombatManager.enemy.rect.midleft[1], *self._cup)
            coffee_cup.start_flip()  # Inicia a animação
            self.cups_created = True

        self._duration_counter += 1

        # Atualiza xícaras e gotas
        self._cup.update()
        self._drops.update()

        # Criando gotas aleatoriamente
        if random.random() < 0.1:  # Chance de 10% por frame
            for cup in self._cup:
                if cup.flipping:  # Gera gotas apenas se a xícara está virando
                    drop = CoffeeDrop(cup.rect.centerx, cup.rect.bottom, self._drops)

        # Verificando colisões com o jogador
        collisions = pygame.sprite.spritecollide(
            self._player, self._drops, dokill=True, collided=pygame.sprite.collide_mask
        )
        if collisions:
            self._player.take_damage(CombatManager.enemy.damage)

        # Retorna `False` se o ataque terminou
        return self._duration_counter < self._duration

    def restart(self):
        """
        Reinicia o ataque, zerando o contador de duração e recriando as xícaras.
        """
        self._duration_counter = 0
        self.cups_created = False
        self._cup.empty()
        self._drops.empty()

    def draw(self, surface):
        """
        Desenha as xícaras e as gotas na superfície fornecida.

        Args:
            surface (pygame.Surface): Superfície onde os elementos serão desenhados.
        """
        self._cup.draw(surface)
        self._drops.draw(surface)

    @property
    def player(self):
        return self._player

    @property
    def duration(self):
        return self._duration

    @property
    def duration_counter(self):
        return self._duration_counter

class PythonAtatack(Attack):
    def __init__(self):
        self.__player: Heart = CombatManager.get_variable('player')

        self.snakes_group = pygame.sprite.Group()

        CombatManager.global_groups.append(self.snakes_group)

        self.snakes: list[Snake] = []
        self.snakes_creation_rate = FPS/5  # 3 Vetores a cada segundo serão criados

        self.__duration = FPS * 10  # O Ataque dura 10 segundos
        self.__duration_counter = 0

    def run(self):
        self.__duration_counter += 1

        if self.__duration_counter % self.snakes_creation_rate == 0:
            self.snakes.append(Snake(self.snakes_group))
        
        if self.__duration_counter >= self.__duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            self.snakes_group.empty()
        
        for snake in self.snakes:
            snake.update(player_center=self.player.rect.center)
        
        for snake in self.snakes_group:
            if self.__player != snake:
                if self.__player.rect.colliderect(snake.rect):
                    offset = (snake.rect.x - self.__player.rect.x, snake.rect.y - self.__player.rect.y)
                    if self.__player.mask.overlap(snake.mask, offset):
                        self.__player.take_damage(CombatManager.enemy.damage)
                        if snake.type == 'Vanished':
                            self.__player.apply_effect('vanished')
                        snake.kill()
        
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

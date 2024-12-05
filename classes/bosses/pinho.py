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
from classes.bosses.attacks.coffee import *

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
            PythonAtatack(),
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

        self.__dead = False
        self.__death_animation_counter = 0
        self.__death_explosions: list[Explosion] = []
        self.death_loops_counter = 255
        self.moment = 0

    def speak(self):
        """
        Função que faz a fala do boss
        """
        if not self.__dead:
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
        if self.__state == 'shaking':
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
            self.__dead = True
        self.__state = 'shaking'
        self.__counter = 0
    
    @property
    def attacks(self):
        return self.__attacks

    @property
    def dead(self):
        return self.__dead

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


class CoffeeAttack(Attack):
    def __init__(self):
        super().__init__()
        self._player: Heart = CombatManager.get_variable('player')
        self._duration = FPS * 10  # O ataque dura 10 segundos
        self._duration_counter = 0
        self.drops_creation_rate = FPS // 5
        self.cups_created = False

        # Criando os grupos
        self.cup_group = pygame.sprite.Group()
        self.drops_group = pygame.sprite.Group()

        # Criando o retângulo do café
        self.battle_container = CombatManager.get_variable('battle_container')
        self.new_rect =  pygame.Rect(
                self.battle_container.inner_rect.left,
                self.battle_container.inner_rect.bottom,
                self.battle_container.inner_rect.width,
                0
        )
        self.new_rect.bottom = self.battle_container.inner_rect.bottom

        self.fill_speed = 3

        self.max_drops = 60

        # Adicionando os grupos aos grupos globais
        CombatManager.global_groups.append(self.cup_group)
        CombatManager.global_groups.append(self.drops_group)

    def create_cups(self):

        # Criando as animações das xícaras
        coffee_cup1 = CoffeeCup(CombatManager.enemy.rect.midleft[0], CombatManager.enemy.rect.midleft[1]-50, self.drops_group, self.cup_group)
        coffee_cup2 = CoffeeCup(CombatManager.enemy.rect.center[0], CombatManager.enemy.rect.center[1]-50, self.drops_group, self.cup_group)
        coffee_cup3 = CoffeeCup(CombatManager.enemy.rect.midright[0], CombatManager.enemy.rect.midright[1]-50, self.drops_group, self.cup_group)

        coffee_cup1.start_flip()
        coffee_cup2.start_flip()
        coffee_cup3.start_flip()

        self.cups_created = True

    def run(self):
        self._duration_counter += 1
        # Criando xícaras se ainda não foram criadas
        if not self.cups_created:
            self.create_cups()

        # Atualiza os grupos
        self.cup_group.update()
        self.drops_group.update()

        self.new_rect.width = self.battle_container.inner_rect.width
        self.new_rect.left = self.battle_container.inner_rect.left

        for cup in self.cup_group:

            # Gera gotas regularmente enquanto as xícaras estão girando
            if cup.flipping and self._duration_counter % int(self.drops_creation_rate) == 0:
                drop = CoffeeDrop(self.drops_group)

            # Gera gotas regularmente para o resto do ataque
            if self._duration_counter % int(self.drops_creation_rate) == 0 and random.random()<0.4:
                drop = CoffeeDrop(self.drops_group)

        # Verifica colisões com o jogador
        collisions = pygame.sprite.spritecollide(
            self._player, self.drops_group, dokill=True, collided=pygame.sprite.collide_mask
        )
        if collisions:
            SoundManager.play_sound("arrow.wav")
            self._player.take_damage(CombatManager.enemy.damage)

        # Atualizando o retângulo
        self.new_rect.height += self.fill_speed * len(collisions)
        if self.new_rect.height >= 250:
            self.new_rect.height = 250
        
        for drop in self.drops_group:
            if drop.rect.y >= self.battle_container.inner_rect.bottom:
                # Incrementa a altura do retângulo de acordo com a quantidade de gotas
                self.new_rect.height += self.fill_speed

                # Ajusta a posição vertical para crescer de baixo para cima
                self.new_rect.top = self.battle_container.inner_rect.bottom - self.new_rect.height

                # Garante que a altura não ultrapasse o limite
                if self.new_rect.height >= 250:
                    self.new_rect.height = 250
                    self.new_rect.top = self.battle_container.inner_rect.bottom - 250
                
                # Ajusta a colisão
                if self.new_rect.colliderect(self._player.rect):
                    SoundManager.play_sound("arrow.wav")
                    self._player.take_damage(CombatManager.enemy.damage)
                
                # Matando os sprites
                drop.kill()

        # Desenhando tudo
        self.draw(pygame.display.get_surface())
        
        # Finaliza o ataque apenas quando o tempo terminar e as gotas desaparecerem
        if self._duration_counter >= self._duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            self.cup_group.empty()
            self.drops_group.empty()
            self.drops_group.empty()
            CombatManager.global_draw_functions.remove(self.draw_puddle)

    # Reinicia o ataque quando necessário   
    def restart(self):
        self._duration_counter = 0
        self.cups_created = False
        self.cup_group.empty()
        self.drops_group.empty()
        self.drops_group.empty()
        CombatManager.global_groups.remove(self.cup_group)
        CombatManager.global_groups.remove(self.drops_group)
        self.cup_group = pygame.sprite.Group()
        self.drops_group = pygame.sprite.Group()
        CombatManager.global_groups.append(self.cup_group)
        CombatManager.global_groups.append(self.drops_group)
        self.new_rect.height = 0  # Reinicia o preenchimento
        CombatManager.global_draw_functions.append(self.draw_puddle)
        self.new_rect =  pygame.Rect(
                self.battle_container.inner_rect.left,
                self.battle_container.inner_rect.bottom,
                self.battle_container.inner_rect.width,
                0
        )

    def draw_puddle(self, *args, **kwargs):
        pygame.draw.rect(pygame.display.get_surface(), (133, 77, 67), self.new_rect)

    # Desenha tudo na tela
    def draw(self, surface):
        self.cup_group.draw(surface)
        self.drops_group.draw(surface)

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

        # Pegando o personagem
        self.__player: Heart = CombatManager.get_variable('player')

        # Criando o grupo 
        self.snakes_group = pygame.sprite.Group()

        # Adicionando no grupo global
        CombatManager.global_groups.append(self.snakes_group)

        # 3 cobras a cada segundo serão criadas
        self.snakes: list[Snake] = []
        self.snakes_creation_rate = FPS/5 

        # O Ataque dura 10 segundos
        self.__duration = FPS * 10 
        self.__duration_counter = 0

    def run(self):
        self.__duration_counter += 1

        if self.__duration_counter % self.snakes_creation_rate == 0:
            self.snakes.append(Snake(self.snakes_group))
        
        # Verifica o turno com base na duração do ataque
        if self.__duration_counter >= self.__duration:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            self.snakes_group.empty()
            self.snakes.clear()
        
        # Atualiza as cobras
        for snake in self.snakes:
            snake.update(player_center=self.player.rect.center)
        
        # Verifica colisões e aplica o efeito
        for snake in self.snakes_group:
            if self.__player.rect.colliderect(snake.rect):
                offset = (snake.rect.x - self.__player.rect.x, snake.rect.y - self.__player.rect.y)
                if self.__player.mask.overlap(snake.mask, offset):
                    self.__player.take_damage(CombatManager.enemy.damage)
                    if snake.type == 'Vanished':
                        self.__player.apply_effect('vanished')
                    snake.kill()
        
    # Reinicia o aqtaque quando necessário
    def restart(self):
        self.__duration_counter = 0
        self.snakes_group.empty()
        self.snakes.clear()

    @property
    def player(self):
        return self.__player

    @property
    def duration(self):
        return self.__duration

    @property
    def duration_counter(self):
        return self.__duration_counter

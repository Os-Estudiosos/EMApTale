import pygame
import os

from config import *
from config.combatmanager import CombatManager
from config.soundmanager import SoundManager

from constants import STOP_HEART_COLOR, MOVE_HEART_COLOR


class Slash(pygame.sprite.Sprite):
    def __init__(self, dir, cut_type,  *groups):
        super().__init__(*groups)

        self.scale = 3.5

        self.display = pygame.display.get_surface()

        self.sprites = [
            pygame.transform.flip(
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'slash_1.png')),
                    self.scale
                ),
                bool(dir+1),
                False
            ),
            pygame.transform.flip(
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'slash_2.png')),
                    self.scale
                ),
                bool(dir+1),
                False
            ),
            pygame.Surface((1,1))
        ]

        # Pintando os sprites a partir do tipo passado
        tint_surface = pygame.Surface(self.sprites[1].get_size())
        tint_surface.fill(STOP_HEART_COLOR if cut_type == 'stop' else MOVE_HEART_COLOR)
        for i in range(len(self.sprites)):
            self.sprites[i].blit(tint_surface, (0,0), special_flags=pygame.BLEND_RGB_MULT)

        self.dir = dir
        self.type = cut_type

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(
            self.display.get_width()//2,
            self.display.get_height()//2-100
        ))

        self.actual_sprite = 0

        self.animating = True

        self.timer_counter = 0  # Contador para trocar de sprite
        self.timer_execution = FPS/20  # Em quanto tempo vai trocar de sprite

    def update(self, *args, **kwargs):
        self.timer_counter += 1
        if self.timer_counter >= self.timer_execution and self.animating:
            self.timer_counter = 0
            if self.actual_sprite + 1 < len(self.sprites):
                self.actual_sprite += 1
            else:
                self.animating = False
            self.image = self.sprites[self.actual_sprite]


class IntegralSword(pygame.sprite.Sprite):
    def __init__(self, initial_angle: int = 0, *groups):
        super().__init__(*groups)

        self.initial_angle = initial_angle

        self.scale = 10
        
        self.slash_group = pygame.sprite.Group()

        self.cuts_amount = 1

        CombatManager.global_groups.append(self.slash_group)
        self.player = CombatManager.get_variable('player')

        self.moving = False

        self.cuts_list: list[Slash] = []

        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, self.initial_angle)
        self.rect = self.image.get_rect()
    
    def rotate_image_to(self, angle):
        self.image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'effects', 'integral.png'))
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def restart(self):
        self.cuts_list.clear()
        self.slash_group.empty()
    
    def update(self):
        for slash in self.cuts_list:
            slash.update()
            if slash.rect.colliderect(self.player.rect) and slash.animating:
                if (
                    (slash.type == 'movement' and self.player.direction.length() == 0)
                    or
                    (slash.type == 'stop' and self.player.direction.length() != 0)
                ):
                    self.player.take_damage(CombatManager.enemy.damage)
    
    def cut(self, type):
        if len(self.cuts_list) < 5:
            SoundManager.play_sound('cinematiccut.wav')
            self.rotate_image_to(180*(self.cuts_amount-1))
            self.cuts_amount += 1
            self.cuts_list.append(Slash((-1)**self.cuts_amount, type, self.slash_group))
            self.rect.centerx = CombatManager.enemy.rect.centerx+(100+CombatManager.enemy.rect.width//2)*(-1)**self.cuts_amount

    def go_to(self, coordinate: tuple[int]):
        vector = pygame.math.Vector2(
            coordinate[0] - self.rect.centerx,
            coordinate[1] - self.rect.centery
        )

        if vector.length() > 10:
            vector = vector.normalize()

            self.rect.x += vector.x*5
            self.rect.y += vector.y*5
            self.moving = True
        else:
            self.moving = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

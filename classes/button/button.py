import pygame
import os
from config import GET_PROJECT_PATH


class CombatButton(pygame.sprite.Sprite):
    def __init__(self, type, button_on_click, display, cursor, groups, activated = False):
        super().__init__(groups)

        self.sprites = {
            'activated': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', f'yellow-{type}.png')),
                1.4
            ),
            'normal': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', f'orange-{type}.png')),
                1.4
            )
        }

        self.display: pygame.Surface = display
        self.activated = activated

        self.image = self.sprites['activated' if activated else 'normal']
        self.rect = self.image.get_rect()

        self.cursor_sprite: pygame.Surface = cursor
        self.cursor_rect = self.cursor_sprite.get_rect()


    def update(self, *args, **kwargs):
        self.image = self.sprites['activated' if self.activated else 'normal']

        # Alterar lugar onde o cursor está sendo desenhado posterioremente
        self.cursor_rect.center = (
            self.rect.centerx - 55,
            self.rect.centery
        )

        if self.activated:
            self.display.blit(self.cursor_sprite, self.cursor_rect)
        return super().update(*args, **kwargs)

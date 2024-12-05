import pygame
import os
from config import GET_PROJECT_PATH
import types


class CombatButton(pygame.sprite.Sprite):
    """Classe que representa o botão das opções do combate
    """
    def __init__(self, type: str, button_on_click: types.FunctionType, display: pygame.Surface, groups: tuple[pygame.sprite.Group], activated: bool = False):
        super().__init__(groups)

        # Dicionário contendo os sprites do botão
        self.sprites = {
            'activated': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', f'yellow-{type}.png')),
                1.7
            ),
            'normal': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'combat', f'orange-{type}.png')),
                1.7
            )
        }

        self.func = button_on_click

        # Definindo as propriedades padrão
        self.display: pygame.Surface = display
        self.__activated = activated

        self.image = self.sprites['activated' if activated else 'normal']  # Sprite atual
        self.rect = self.image.get_rect()  # Retângulo do sprite

    def on_click(self):
        self.func()
    
    @property
    def activated(self):
        return self.__activated

    @activated.setter
    def activated(self, value):
        # Definindo a imagem com base no sprite
        self.image = self.sprites['activated' if value else 'normal']
        
        self.__activated = value

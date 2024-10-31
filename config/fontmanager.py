import pygame
import os
from config import GET_PROJECT_PATH


class FontManager:
    def __init__(self):
        pygame.font.init()

        self.fonts = {
            'Game-Font': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Game-Font.ttf'),
            'Gamer': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Gamer.ttf'),
        }

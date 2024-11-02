import pygame
import os
from config import GET_PROJECT_PATH


class FontManager:
    """Classe responsável por armazenas o caminho de todas as fontes
    (Não carrega a fonte direto pois eu posso querer usar várias cores, tamanhos e etc.)
    """
    def __init__(self):
        pygame.font.init()

        self.fonts = {
            'Game-Font': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Game-Font.ttf'),
            'Gamer': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Gamer.ttf'),
        }

import pygame
from utils import sign


class BattleContainer:
    """Classe que representa o container que o coração do jogador fica
    """
    def __init__(self, display: pygame.Surface):
        """Inicialização

        Args:
            display (pygame.Surface): Janela que ele vai ser desenhado (Pra ja ficar armazenado bonitinho)
        """
        self.display = display
        self.out_rect = pygame.Rect(0, 0, 1000, 300)
        self.out_rect_color = pygame.Color(255, 255, 255)
        self.inner_rect = pygame.Rect(0, 0, self.out_rect.width-10, self.out_rect.height-10)
        self.inner_rect_color = pygame.Color(0,0,0)

        self.out_rect.center = (self.display.get_width()/2, self.display.get_height()/2 + 50)
        self.inner_rect.center = self.out_rect.center

        self.resize_counter = 0  # Contador para o controle do redimensionamento
        self.resize_new_width = 0
        self.resize_new_height = 0
        self.resizing = False

    def update(self):
        """Função que vai rodar em todo loop do jogo
        """

        if self.resizing:
            self.out_rect.height += 10 * sign(-self.out_rect.height + self.resize_new_height)
            self.out_rect.width += 10 * sign(-self.out_rect.width + self.resize_new_width)

            self.inner_rect.size = (self.out_rect.width-10, self.out_rect.height-10)
            
            if self.out_rect.width == self.resize_new_width and self.out_rect.height == self.resize_new_height:
                self.resizing = False

    def draw(self):
        """Função que desenha as caixas
        """
        pygame.draw.rect(self.display, self.out_rect_color, self.out_rect)
        pygame.draw.rect(self.display, self.inner_rect_color, self.inner_rect)

    def resize(self, new_width: float, new_height: float):
        """Função responsável por redimensionar dinamicamente o tamanho da caixa

        Args:
            new_width (float): Nova Largura
            new_height (float): Nova Altura
        """
        self.resizing = True
        self.resize_new_height = new_height
        self.resize_new_width = new_width

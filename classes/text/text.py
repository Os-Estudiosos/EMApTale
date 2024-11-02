import pygame

class Text:
    """Classe para facilitar a plotagem de textos na tela
    """
    def __init__(self, text: str, font: str, size: int = 12, color: pygame.Color = (255, 255, 255)):
        """Inicialização da classe

        Args:
            text (str): Qual o texto deve ser exibido
            font (str): O nome da fonte que vai ser usada (Olhar no gerenciador de fontes)
            size (int, optional): Tamanho da fonte. Defaults to 12.
            color (pygame.Color, optional): Cor da fonte. Defaults to (255, 255, 255).
        """
        font_obj = pygame.font.Font(font, size)
        self.img: pygame.Surface = font_obj.render(text, True, color)
        self.rect = self.img.get_rect()
    
    def draw(self, surface: pygame.Surface):
        """Método responsável por desenhar o texto na superfície passada

        Args:
            surface (pygame.Surface): Superfície onde o texto deve ser desenhado
        """
        surface.blit(self.img, self.rect)

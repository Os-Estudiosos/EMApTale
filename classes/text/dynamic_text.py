import pygame
from config import FPS


class DynamicText(pygame.sprite.Sprite):
    """Classe mostra o texto dinamicamente, letra por letra
    """
    def __init__(self, text: str, font: str, letters_per_second: int, size: int = 12, groups: list[pygame.sprite.Sprite] = [], positon: tuple[float] = (0,0), color: pygame.Color = (255,255,255)):
        """Inicialização da classe

        Args:
            text (str): Qual o texto deve ser exibido
            font (str): O nome da fonte que vai ser usada (Olhar no gerenciador de fontes)
            size (int, optional): Tamanho da fonte. Defaults to 12.
            color (pygame.Color, optional): Cor da fonte. Defaults to (255, 255, 255).
            letters_per_second (int): Quantas letras aparecem por segundo
        """
        super().__init__(*groups)

        self.text = text  # Texto
        self.progressive_text = ''  # O texto que vai ser exibido
        self.letter_counter = 0  # Qual a próxima letra a ser adicionada
        self.font = pygame.font.Font(font, size) # Fonte que vai ser usada
        self.color = color  # Cor da fonte
        self.image: pygame.Surface = self.font.render(self.progressive_text, True, self.color)  # Imagem do texto
        self.rect = self.image.get_rect()  # Retângulo da imagem
        self.position = positon

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.counter = 0  # Variável que controla quando uma nova letra vai ser adicionada
        self.letter_rate = FPS/letters_per_second  # Frequência de letras por segundo
    
    def update(self, *args, **kwargs):
        self.counter += 1  # Aumenta a contagem
        
        # Se a montagem for maior que a frequência das letras e o contador de letras não for maior que a quantidade de letras
        if self.counter >= self.letter_rate and not self.letter_counter >= len(self.text):
            self.counter = 0  # Zera o contador
            self.progressive_text += self.text[self.letter_counter]  # Altero o texto
            self.letter_counter += 1  # Aumento o contador da letra
            self.image = self.font.render(self.progressive_text, True, self.color)  # Mudo a imagem do texto
            self.rect = self.image.get_rect()
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

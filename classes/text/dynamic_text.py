import pygame
from config import FPS

from config.soundmanager import SoundManager


class DynamicText:
    """Classe mostra o texto dinamicamente, letra por letra
    """
    def __init__(
        self,
        text: str,
        font: str,
        letters_per_second: int,
        text_size: int = 12,
        max_length: float = 0,
        positon: tuple[float] = (0,0),
        color: pygame.Color = (255,255,255)
    ):
        """Inicialização da classe

        Args:
            text (str): Qual o texto deve ser exibido
            font (str): O nome da fonte que vai ser usada (Olhar no gerenciador de fontes)
            size (int, optional): Tamanho da fonte. Defaults to 12.
            color (pygame.Color, optional): Cor da fonte. Defaults to (255, 255, 255).
            letters_per_second (int): Quantas letras aparecem por segundo
        """

        self.text = text  # Texto Completo
        self.progressive_text = ''
        self.font = pygame.font.Font(font, text_size)

        self.max_length = max_length
        self.position = positon
        self.color = color

        self.list_texts = [
            self.font.render(self.progressive_text, True, self.color)
        ]
        self.wich_text_to_update = 0
        self.letter_counter = 0

        self.counter = 0  # Variável que controla quando uma nova letra vai ser adicionada
        self.letter_rate = FPS/letters_per_second  # Frequência de letras por segundo
    
    def update(self, *args, **kwargs):
        self.counter += 1  # Aumenta a contagem
        
        # Se a montagem for maior que a frequência das letras e o contador de letras não for maior que a quantidade de letras
        if self.counter >= self.letter_rate and not self.letter_counter >= len(self.text):
            self.counter = 0  # Zera o contador

            self.progressive_text += self.text[self.letter_counter]

            new_text = self.font.render(self.progressive_text, True, self.color)

            if new_text.get_rect().width >= self.max_length:
                self.progressive_text = self.text[self.letter_counter]
                self.list_texts.append(self.font.render(self.progressive_text, True, self.color))
                self.wich_text_to_update += 1

            self.list_texts[self.wich_text_to_update] = new_text

            self.letter_counter += 1
        
    def draw(self, screen: pygame.Surface):
        for i, text in enumerate(self.list_texts):
            text_rect = text.get_rect()
            text_rect.x = self.position[0]
            text_rect.y = self.position[1]+i*text_rect.height
            screen.blit(text, text_rect)


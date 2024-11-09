import pygame
from config import FPS
from config.soundmanager import SoundManager

class DynamicText:
    """Classe mostra o texto dinamicamente, letra por letra."""
    def __init__(
        self,
        text: str,
        font: str,
        letters_per_second: int,
        text_size: int = 12,
        max_length: float = 0,
        position: tuple[float] = (0, 0),
        color: pygame.Color = (255, 255, 255)
    ):
        """Inicialização da classe
            
        Args:
            text (str): Qual o texto deve ser exibido
            font (str): O nome da fonte que vai ser usada (Olhar no gerenciador de fontes)
            letters_per_second (int): Quantas letras aparecem por segundo
            text_size (int, optional): Tamanho da fonte. Defaults to 12.
            max_length (float, optional): Largura máxima do texto. Defaults to 0.
            position (tuple, optional): Posição do texto na tela. Defaults to (0, 0).
            color (pygame.Color, optional): Cor da fonte. Defaults to (255, 255, 255).
        """
        self.text = text
        self.progressive_text = ''
        self.font = pygame.font.Font(font, text_size)
        self.max_length = max_length
        self.position = position
        self.color = color

        self.rows = [self.font.render(self.progressive_text, True, self.color)]
        self.wich_row_to_update = 0
        self.letter_counter = 0

        self.counter = 0
        self.letter_rate = FPS / letters_per_second

        self.finished = False  # Indica se terminou de escrever o texto
    
    def update(self):
        if self.finished:
            return

        self.counter += 1
        if self.counter >= self.letter_rate and self.letter_counter < len(self.text):
            if self.text[self.letter_counter] != ' ':
                SoundManager.play_sound('text.wav')
                
                
            self.counter = 0
            self.progressive_text += self.text[self.letter_counter]
            new_text = self.font.render(self.progressive_text, True, self.color)

            if new_text.get_rect().width >= self.max_length and self.max_length > 0:
                self.progressive_text = self.text[self.letter_counter]
                self.rows.append(self.font.render(self.progressive_text, True, self.color))
                self.wich_row_to_update += 1
                new_text = self.font.render(self.progressive_text, True, self.color)

            self.rows[self.wich_row_to_update] = new_text
            self.letter_counter += 1

            # Verificar se terminou de escrever o texto
            if self.letter_counter >= len(self.text):
                self.finished = True
        
    def draw(self, screen: pygame.Surface):
        for i, text in enumerate(self.rows):
            text_rect = text.get_rect()
            text_rect.x = self.position[0]
            text_rect.y = self.position[1] + i * text_rect.height
            screen.blit(text, text_rect)
    
    @property
    def is_finished(self):
        return self.finished

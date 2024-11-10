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
        color: pygame.Color = (255,255,255),
        sound: bool = True
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
        self.progressive_text = ''  # Texto que vai ser alterado para dar o efeito de letra por letra
        self.font = pygame.font.Font(font, text_size)  # Fonte que vai ser usada

        self.max_length = max_length  # Largura máxima
        self.position = positon  # Posição do texto
        self.color = color  # Cor do texto

        self.rows = [  # Lista que vai contar as linhas
            self.font.render(self.progressive_text, True, self.color)
        ]
        self.wich_row_to_update = 0  # Qual linha está sendo atualizada
        self.letter_counter = 0  # Contador para saber a próxima letra

        self.counter = 0  # Variável que controla quando uma nova letra vai ser adicionada
        self.letter_rate = FPS/letters_per_second  # Frequência de letras por segundo

        self.sound = sound

    
    def update(self, *args, **kwargs):
        self.counter += 1  # Aumenta a contagem
        
        # Se a montagem for maior que a frequência das letras e o contador de letras não for maior que a quantidade de letras
        if self.counter >= self.letter_rate and not self.letter_counter >= len(self.text):
            if self.text[self.letter_counter] != ' ' and self.sound:
                SoundManager.stop_sound('text.wav')
                SoundManager.play_sound('text.wav')
            
            self.counter = 0  # Zera o contador

            self.progressive_text += self.text[self.letter_counter]

            new_text = self.font.render(self.progressive_text, True, self.color)

            if new_text.get_rect().width >= self.max_length:  # Se a linha passar da largura máxima
                self.progressive_text = self.text[self.letter_counter]
                self.rows.append(self.font.render(self.progressive_text, True, self.color))
                self.wich_row_to_update += 1

                new_text = self.font.render(self.progressive_text, True, self.color)

            # Atualizo a linha com o novo texto
            self.rows[self.wich_row_to_update] = new_text

            # Atualizo a próxima letra
            self.letter_counter += 1
        
    def draw(self, screen: pygame.Surface):
        for i, text in enumerate(self.rows):
            text_rect = text.get_rect()
            text_rect.x = self.position[0]
            text_rect.y = self.position[1]+i*text_rect.height
            screen.blit(text, text_rect)


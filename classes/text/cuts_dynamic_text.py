import pygame
from config import FPS
from config.soundmanager import SoundManager

class CDynamicText:
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
        """Inicialização da classe"""
        self.words = text.split()  # Divide o texto em palavras
        self.progressive_text = ''
        self.font = pygame.font.Font(font, text_size)
        self.max_length = max_length
        self.position = position
        self.color = color

        self.rows = [self.font.render(self.progressive_text, True, self.color)]
        self.wich_row_to_update = 0
        self.current_word = ''
        self.letter_counter = 0

        self.counter = 0
        self.letter_rate = FPS / letters_per_second

        self.finished = False  # Indica se terminou de escrever o texto
    
    def update(self):
        if self.finished:
            return

        if self.letter_counter >= len(self.current_word):
            # Começa uma nova palavra se necessário
            if self.words:
                self.current_word = self.words.pop(0) + ' '  # Adiciona espaço ao final da palavra
                # Testa se a palavra inteira cabe na linha atual
                projected_text = self.progressive_text + self.current_word
                rendered_text = self.font.render(projected_text, True, self.color)
                
                if self.max_length > 0 and rendered_text.get_rect().width > self.max_length:
                    # Começa uma nova linha se a palavra não couber
                    self.progressive_text = ''
                    self.rows.append(self.font.render(self.progressive_text, True, self.color))
                    self.wich_row_to_update += 1

                self.letter_counter = 0  # Reinicia o contador de letras da nova palavra

            else:
                # Se não há mais palavras, o texto terminou
                self.finished = True
                return

        # Exibe a próxima letra da palavra atual
        self.counter += 1
        if self.counter >= self.letter_rate:
            self.counter = 0
            self.progressive_text += self.current_word[self.letter_counter]
            self.letter_counter += 1

            # Atualiza a linha atual com o texto progressivo
            self.rows[self.wich_row_to_update] = self.font.render(self.progressive_text, True, self.color)
    
    def draw(self, screen: pygame.Surface):
        for i, text in enumerate(self.rows):
            text_rect = text.get_rect()
            text_rect.x = self.position[0]
            text_rect.y = self.position[1] + i * text_rect.height
            screen.blit(text, text_rect)
    
    @property
    def is_finished(self):
        return self.finished

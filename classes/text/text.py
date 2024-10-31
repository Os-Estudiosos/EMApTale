import pygame

class Text:
    def __init__(self, text: str, font: str, size: int = 12, color: pygame.Color = (255, 255, 255)):
        font_obj = pygame.font.Font(font, size)
        self.img: pygame.Surface = font_obj.render(text, True, color)
        self.rect = self.img.get_rect()
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

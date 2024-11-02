import pygame


class BattleContainer:
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.out_rect = pygame.Rect(0, 0, 400, 300)
        self.out_rect_color = pygame.Color(255, 255, 255)
        self.inner_rect = pygame.Rect(0, 0, self.out_rect.width-10, self.out_rect.height-10)
        self.inner_rect_color = pygame.Color(0,0,0)

    def update(self):
        self.out_rect.center = (self.display.get_width()/2, self.display.get_height()/2 + 50)
        self.inner_rect.center = self.out_rect.center

    def draw(self):
        pygame.draw.rect(self.display, self.out_rect_color, self.out_rect)
        pygame.draw.rect(self.display, self.inner_rect_color, self.inner_rect)

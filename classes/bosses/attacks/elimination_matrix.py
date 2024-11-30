import pygame

from classes.text.text import Text
from classes.bosses.attacks.horizontal_beam import HorizontalBeam


class ElimiationMatrix(Text):
    def __init__(self, text, font, associated_beam: HorizontalBeam, size = 12, color = (255,255,255)):
        super().__init__(text, font, size, color)
        self.associated_beam = associated_beam
        self.rect.x = -100
        self.finished = False

    def update(self, squared_bracket_right):
        self.rect.centery = squared_bracket_right.rect.centery

        if self.associated_beam.alpha <= 100 and not self.associated_beam.animating:
            self.rect.x = self.associated_beam.alpha + 100 - self.rect.width*2
        else:
            self.finished = False
            self.rect.x = -100

    def draw(self, surface):
        return super().draw(surface)


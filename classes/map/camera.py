import pygame
from classes.polygon.polygon import Polygon

class Camera(pygame.sprite.Group):
    """Controla a área visível do mapa em relação ao jogador
    """
    def __init__(self, map_width, map_height, screen_width, screen_height, *sprites):
        """Inicializa a câmera com as dimensões do mapa e da tela

        Args:
            map_width (int): Largura total do mapa
            map_height (int): Altura total do mapa
            screen_width (int): Largura da tela de exibição
            screen_height (int): Altura da tela de exibição
        """
        super().__init__(*sprites)
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, entity: pygame.Rect | pygame.sprite.Sprite):
        """Aplica a posição da câmera a uma entidade, ajustando sua posição"""
        if isinstance(entity, pygame.Rect):
            return entity.move(-self.camera_rect.x, -self.camera_rect.y)
        if isinstance(entity, Polygon):
            return entity.move(-self.camera_rect.x, -self.camera_rect.y)
        if isinstance(entity, (list, tuple)):
            return [entity[0] - self.camera_rect.x, entity[1] - self.camera_rect.y]
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_ysort(self, renderables: list):
        """
        Ordena e ajusta os itens para renderização com base na profundidade (Y-Sort).
        """
        renderables.sort(key=lambda item: item[0])
        return [
            (y, image, self.apply(rect)) for y, image, rect in renderables
        ]

    def update(self, target_rect: pygame.Rect, *args, **kwargs):
        """Atualiza a posição da câmera em relação ao jogador, otimizando os cálculos."""
        super().update(*args, **kwargs)

        x = target_rect.centerx - self.screen_width // 2
        y = target_rect.centery - self.screen_height // 2

        # Limita a câmera para que ela não saia dos limites do mapa
        x = max(0, min(x, self.map_width - self.screen_width))
        y = max(0, min(y, self.map_height - self.screen_height))

        # Atualiza a posição da câmera com base no jogador
        self.camera_rect.x = x
        self.camera_rect.y = y
    
    def draw(self, surface, bgsurf = None, special_flags = 0):
        for sprite in self.sprites():
            surface.blit(sprite.image, self.apply(sprite.rect))

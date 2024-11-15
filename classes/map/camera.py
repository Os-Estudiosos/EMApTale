import pygame

from classes.polygon.polygon import Polygon


class Camera:
    """Controla a área visível do mapa em relação ao jogador
    """
    def __init__(self, map_width, map_height, screen_width, screen_height):
        """Inicializa a câmera com as dimensões do mapa e da tela

        Args:
            map_width (int): Largura total do mapa
            map_height (int): Altura total do mapa
            screen_width (int): Largura da tela de exibição
            screen_height (int): Altura da tela de exibição
        """
        self.map_width = map_width  #Largura total do mapa
        self.map_height = map_height  #Altura total do mapa
        self.screen_width = screen_width  #Largura da tela de exibição
        self.screen_height = screen_height  #Altura da tela de exibição
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)  #Define a área da câmera

    def apply(self, entity: pygame.Rect | pygame.sprite.Sprite):
        """Método para aplicar a posição da câmera a uma entidade, ajustando sua posição

        Args:
            entity (pygame.Rect | pygame.sprite.Sprite): A entidade que a câmera vai focar

        Returns:
            pygame.Rect: O retângulo que representa a entidade movida para a câmera
        """
        #Verifica se a entidade é um retângulo (pygame.Rect)
        if isinstance(entity, pygame.Rect):
            #Move a entidade com base na posição da câmera, retornando a posição ajustada
            return entity.move(-self.camera_rect.x, -self.camera_rect.y)
        if isinstance(entity, Polygon):
            return entity.move(-self.camera_rect.x, -self.camera_rect.y)
        if isinstance(entity, list) or isinstance(entity, tuple):
            return [
                entity[0] - self.camera_rect.x,
                entity[1] - self.camera_rect.y
            ]
        #Se a entidade não for pygame.Rect, usa a propriedade rect para mover
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target_rect: pygame.Rect):
        """Método para atualizar a posição da câmera em relação ao jogador

        Args:
            target_rect (pygame.Rect): O retângulo que eu quero que a câmera acompanhe
        """
        #Centraliza a câmera no centro do jogador (target_rect)
        x = target_rect.centerx - self.screen_width // 2
        y = target_rect.centery - self.screen_height // 2

        #Limita a câmera para que ela não saia dos limites do mapa
        x = max(0, min(x, self.map_width - self.screen_width))
        y = max(0, min(y, self.map_height - self.screen_height))

        #Atualiza a posição da câmera com a nova posição calculada
        self.camera_rect = pygame.Rect(x, y, self.screen_width, self.screen_height)
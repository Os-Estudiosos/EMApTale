from pytmx import load_pygame
import pygame
# import math

from classes.polygon.polygon import Polygon


#Carrega e renderiza mapas do tipo .tmx
class MapLoader:
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)  # Carrega o mapa usando pytmx
        self.scale_factor = 2.5  # Fator de escala para o mapa e colisões
        self.offset_vector = pygame.math.Vector2(-100, -150)  # Deslocamento dos blocos de colisão
        self.walls = self.load_walls()  # Carrega as áreas de colisão do mapa

    def render_with_vector(self, surface, camera, vector):
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        pos = (
                            x * self.tmx_data.tilewidth * self.scale_factor + vector.x,
                            y * self.tmx_data.tileheight * self.scale_factor + vector.y
                        )
                        surface.blit(
                            pygame.transform.scale_by(tile, self.scale_factor),
                            camera.apply(pygame.Rect(*pos, self.tmx_data.tilewidth * self.scale_factor, self.tmx_data.tileheight * self.scale_factor))
                        )

    def render_objects_with_gid(self, surface, camera, vector):
        """
        Renderiza objetos com gid definido no mapa.
        """
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:  # Verifica se o objeto tem gid e está visível
                    # Obtém a imagem do objeto a partir do gid
                    tile_image = self.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        # Aplica o fator de escala e deslocamento
                        pos = (
                            obj.x * self.scale_factor + vector.x,
                            obj.y * self.scale_factor + vector.y
                        )
                        scaled_image = pygame.transform.scale_by(tile_image, self.scale_factor)
                        surface.blit(scaled_image, camera.apply(pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())))

    def load_walls(self):
        walls = []
        for layer in self.tmx_data.layers:
            if layer.name == "WallsColider":
                for obj in layer:
                    # Escala e aplica o deslocamento às áreas de colisão
                    rect = pygame.Rect(
                        obj.x * self.scale_factor + self.offset_vector.x,
                        obj.y * self.scale_factor + self.offset_vector.y,
                        obj.width * self.scale_factor,
                        obj.height * self.scale_factor
                    )
                    walls.append(rect)
            if layer.name == "NotRectWallsColiders":
                for obj in layer:
                    pol = Polygon(obj.points)
                    pol.scale(self.scale_factor)
                    walls.append(pol)
        return walls

    def get_size(self):
        width = self.tmx_data.width * self.tmx_data.tilewidth * self.scale_factor
        height = self.tmx_data.height * self.tmx_data.tileheight * self.scale_factor
        return width, height
from pytmx import load_pygame
import pygame

from config import *
from classes.polygon.polygon import Polygon
from classes.map.interaction import Interaction, BossIntercation
from config.globalmanager import GlobalManager

from classes.item import Item


# Carrega e renderiza mapas do tipo .tmx
class MapLoader:
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)  # Carrega o mapa usando pytmx
        GlobalManager.offset_vector = MAP_OFFSET_VECTOR
        self.walls = self.load_walls()  # Carrega as áreas de colisão do mapa
        self.load_interactions()

    def load_interactions(self):
        """
        Carrega os objetos da camada de interações.
        """
        for layer in self.tmx_data.layers:
            if layer.name == "Interactions":  # Verifica a camada de interações
                for obj in layer:
                    GlobalManager.interactions.append(Interaction(
                        interaction_name=obj.properties.get('interaction_name', 'Unknown'),
                        value=obj.properties.get('value', 'Sem mensagem'),
                        x=obj.x * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.x,
                        y=obj.y * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.y,
                        width=obj.width * MAP_SCALE_FACTOR,
                        height=obj.height * MAP_SCALE_FACTOR,
                        day=obj.properties.get('day', None)
                    ))
            if layer.name == "Boss":
                for obj in layer:
                    GlobalManager.interactions.append(BossIntercation(
                        interaction_name=obj.properties.get('interaction_name', 'Unknown'),
                        value=obj.properties.get('value', 'Sem mensagem'),
                        x=obj.x * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.x,
                        y=obj.y * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.y,
                        width=obj.width * MAP_SCALE_FACTOR,
                        height=obj.height * MAP_SCALE_FACTOR,
                        day=obj.properties.get('day', None),
                        boss=obj.properties.get('boss')
                    ))
    
    def load_items(self):
        for layer in self.tmx_data.layers:
            if layer.name == "Objs":
                for obj in layer:
                    if obj.properties.get('day') == GlobalManager.day:
                        Item(
                            GlobalManager.get_item(obj.properties.get('item_id')),
                            (
                                obj.x,
                                obj.y
                            ),
                            GlobalManager.groups['items'],
                            GlobalManager.camera
                        )

    def render_map(self, surface, camera):
        """
        Renderiza o mapa completo (tiles e objetos).
        :param surface: Superfície onde o mapa será renderizado.
        :param camera: Câmera para ajustar o deslocamento.
        """
        self.render_with_vector(surface, camera, MAP_OFFSET_VECTOR)
        self.render_objects_with_gid(surface, camera, MAP_OFFSET_VECTOR)

    def render_with_vector(self, surface, camera, vector):
        # Calcula os limites visíveis da tela com base na posição da câmera
        screen_rect = pygame.Rect(camera.camera_rect.x, camera.camera_rect.y, camera.screen_width, camera.screen_height)
        
        # Itera sobre as camadas do mapa e renderiza apenas os tiles visíveis
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, tile in layer.tiles():
                    if tile:
                        # Calcula a posição do tile no mapa
                        pos = (
                            x * self.tmx_data.tilewidth * MAP_SCALE_FACTOR + vector.x,
                            y * self.tmx_data.tileheight * MAP_SCALE_FACTOR + vector.y
                        )
                        # Cria um retângulo para o tile
                        rect = pygame.Rect(
                            *pos,
                            self.tmx_data.tilewidth * MAP_SCALE_FACTOR,
                            self.tmx_data.tileheight * MAP_SCALE_FACTOR
                        )
                        
                        # Verifica se o tile está dentro dos limites da tela
                        if screen_rect.colliderect(rect):
                            surface.blit(
                                pygame.transform.scale_by(tile, MAP_SCALE_FACTOR),
                                camera.apply(rect)  # Aplica a câmera diretamente
                            )


    def render_objects_with_gid(self, surface, camera, vector):
        """
        Renderiza objetos com gid definido no mapa.
        """
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:  # Verifica se o objeto tem gid e está visível
                    tile_image = self.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        pos = (
                            obj.x * MAP_SCALE_FACTOR + vector.x,
                            obj.y * MAP_SCALE_FACTOR + vector.y
                        )
                        scaled_image = pygame.transform.scale_by(tile_image, MAP_SCALE_FACTOR)
                        surface.blit(scaled_image, camera.apply(
                            pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())
                        ))

    def load_walls(self):
        """
        Carrega as áreas de colisão do mapa.
        """
        walls = []
        for layer in self.tmx_data.layers:
            if layer.name == "WallsColider":
                for obj in layer:
                    rect = pygame.Rect(
                        obj.x * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.x,
                        obj.y * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.y,
                        obj.width * MAP_SCALE_FACTOR,
                        obj.height * MAP_SCALE_FACTOR
                    )
                    walls.append(rect)
            elif layer.name == "NotRectWallsColiders":
                for obj in layer:
                    if hasattr(obj, "points"):
                        # Processar polígonos
                        adjusted_points = [
                            [p[0] * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.x, p[1] * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.y]
                            for p in obj.points
                        ]
                        pol = Polygon(adjusted_points)
                        walls.append(pol)
        return walls

    def get_renderables(self, player):
        """
        Retorna uma lista de todos os itens renderizáveis (mapa e jogador).
        """
        renderables = []

        # Adiciona objetos do mapa
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                if obj.gid > 0 and obj.visible:
                    tile_image = self.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile_image:
                        pos = (
                            obj.x * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.x,
                            obj.y * MAP_SCALE_FACTOR + MAP_OFFSET_VECTOR.y
                        )
                        scaled_image = pygame.transform.scale_by(tile_image, MAP_SCALE_FACTOR)
                        rect = pygame.Rect(*pos, scaled_image.get_width(), scaled_image.get_height())
                        renderables.append((rect.bottom, scaled_image, rect))

        # Adiciona o jogador
        renderables.append((player.rect.bottom, player, player.rect))

        return renderables

    def get_size(self):
        """
        Retorna o tamanho do mapa em pixels.
        """
        width = self.tmx_data.width * self.tmx_data.tilewidth * MAP_SCALE_FACTOR
        height = self.tmx_data.height * self.tmx_data.tileheight * MAP_SCALE_FACTOR
        return width, height

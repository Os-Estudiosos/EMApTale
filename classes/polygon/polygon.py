import pygame
import numpy as np


class Polygon:
    def __init__(self, points: list[tuple[int]]):
        self.points = list(map(lambda point: [point.x, point.y], points))
        self.previous_position = self.points.copy()
        self.edges = self.finding_edges()

    def colliderect(self, rect: pygame.Rect):
        # Pegando os pontos extremos para obter as arestas:
        rect_edges = [
            # Upper
            (rect.topleft, rect.topright),
            # Left
            (rect.topleft, rect.bottomleft),
            # Right
            (rect.topright, rect.bottomright),
            # Bottom
            (rect.bottomleft, rect.bottomright)
        ]
    
    def __iter__(self):
        return iter(self.points)
    
    def move(self, move_x, move_y):
        self.points = [(x + move_x, y + move_y) for x, y in self.previous_position]
        return self

    def scale(self, factor):
        scale_matrix = np.array([[factor, 0], [0, factor]], dtype=int)
        scaled_points = []

        # Achando o ponto central
        n = len(self.points)
        points_matrix = np.column_stack(self.points.copy())

        center_point = np.dot(points_matrix, np.ones(n)) / n

        for point in self.previous_position:
            point_array = np.array(point, dtype=float) - center_point
            scaled_point = np.dot(scale_matrix, point_array)
            scaled_points.append((scaled_point + center_point).tolist())
        self.previous_position = scaled_points.copy()
        self.points = scaled_points.copy()
        self.edges = self.finding_edges()
    
    def finding_edges(self):
        def cross(o, a, b):
            """Função de Produto vetorial
            """
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        # Ordenar os pontos pela coordenada x, e y em caso de empate
        points = sorted(self.points, key=lambda p: p[0])

        # Construir a parte inferior da casca convexa
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        # Construir a parte superior da casca convexa
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        # Remover o último ponto de cada parte (pois será duplicado)
        hull_points = lower[:-1] + upper[:-1]

        edges = []
        for i in range(len(hull_points)):
            # Conectar o ponto i com o próximo (circularmente)
            edge = (hull_points[i], hull_points[(i + 1) % len(hull_points)])
            edges.append(edge)
        
        return edges

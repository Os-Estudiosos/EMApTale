import pygame
import numpy as np


class Polygon:
    def __init__(self, points: list):
        # Verifica o formato dos pontos
        if isinstance(points[0], (tuple, list)):
            # Se for uma tupla ou lista, converte diretamente
            self.points = [list(point) for point in points]
        elif hasattr(points[0], "x") and hasattr(points[0], "y"):
            # Se for um objeto com atributos x e y
            self.points = [[point.x, point.y] for point in points]
        else:
            raise TypeError("Os pontos devem ser listas/tuplas de coordenadas ou objetos com atributos x e y")
        
        self.edges = self.finding_edges()


    def colliderect(self, rect: pygame.Rect):
        # Definir os eixos do retângulo (horizontal e vertical)
        rect_axes = [np.array([1, 0]), np.array([0, 1])]  # Eixos horizontal e vertical

        # Obter os eixos do polígono (normais às arestas)
        def get_normal(edge):
            p1, p2 = edge
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            return np.array([-dy, dx])  # Normal no plano 2D
        poly_axes = [get_normal(edge) for edge in self.edges]

        def project_points(points, axis):
            projections = [np.dot(p, axis) for p in points]
            return min(projections), max(projections)

        # Combinar todos os eixos (eixos do retângulo + eixos do polígono)
        axes = rect_axes + poly_axes

        # Para cada eixo, projetar o retângulo e o polígono e verificar se as projeções se sobrepõem
        for axis in axes:
            # Normalizar o eixo para garantir que as projeções sejam comparáveis
            axis = axis / np.linalg.norm(axis)

            # Projetar os pontos do retângulo sobre o eixo
            rect_points = [np.array(rect.topleft), 
                        np.array(rect.topright),
                        np.array(rect.bottomleft),
                        np.array(rect.bottomright)]
            
            rect_min, rect_max = project_points(rect_points, axis)

            # Projetar os pontos do polígono sobre o eixo
            poly_min, poly_max = project_points(self.points, axis)

            # Verificar se as projeções se sobrepõem
            if rect_max < poly_min or poly_max < rect_min:
                # Se as projeções não se sobrepõem, significa que há um eixo de separação
                return False
        
        # Se não houver nenhum eixo de separação, significa que os objetos colidiram
        return True
    
    def __iter__(self):
        return iter(self.points)
    
    def move(self, move_x, move_y):
        return Polygon([(x + move_x, y + move_y) for x, y in self.points])

    def scale(self, factor):
        scale_matrix = np.array([[factor, 0], [0, factor]], dtype=int)
        scaled_points = []

        # Achando o ponto central
        n = len(self.points)
        points_matrix = np.column_stack(self.points.copy())

        center_point = np.dot(points_matrix, np.ones(n)) / n

        for point in self.points:
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
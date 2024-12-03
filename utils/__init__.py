import math
import numpy as np


def sign(number: float) -> int:
    """Função que retorna o sinal do número (-1 para negativos, 1 para positivos)

    Args:
        number (float): Número pedido

    Returns:
        int: 1 para positivos, 0 para 0, -1 para negativos
    """
    if number == 0:
        return 0
    elif number < 0:
        return -1
    elif number > 0:
        return 1


def radians_to_degrees(angle: float|int):
    """Função que recebe um angulo em radianos e retorna o resultado em graus

    Args:
        angle (float): O ângulo que desejo substituir
    """
    if not isinstance(angle, int) and not isinstance(angle, float):
        raise TypeError("Você não forneceu um tipo de ângulo válido")
    return angle * (180/math.pi)


def distance_point_and_segment(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula a distância de um ponto até um segmento de reta

    Args:
        px (float): x do ponto
        py (float): y do ponto
        x1 (float): x do ponto A do segmento
        y1 (float): y do ponto A do segmento
        x2 (float): x do ponto B do segmento
        y2 (float): y do ponto B do segmento

    Returns:
        float: A distância entre o ponto e o segmento
    """
    APx, APy = px - x1, py - y1
    ABx, ABy = x2 - x1, y2 - y1
    ab2 = ABx**2 + ABy**2
    ap_ab = APx * ABx + APy * ABy
    t = max(0, min(1, ap_ab / ab2))  # Restringe t ao intervalo [0, 1]
    ponto_mais_proximo_x = x1 + t * ABx
    ponto_mais_proximo_y = y1 + t * ABy
    dist = math.sqrt((px - ponto_mais_proximo_x)**2 + (py - ponto_mais_proximo_y)**2)
    return dist


def line_between_two_points(point1: tuple[float], point2: tuple[float]):
    """Função que calcula a equação da reta entre dois pontos

    Args:
        point1 (tuple[float]): Ponto 1
        point2 (tuple[float]): Ponto 2

    Returns:
        (tuple): Dois coeficientes da reta (m, n) (y = mx + n)
    """
    x1, y1 = point1
    x2, y2 = point2
    m = (y2 - y1) / (x2 - x1)  # Coeficiente angular
    n = y1 - m * x1  # Interseção com o eixo y

    return m, n


def distance_between_point_and_line(point: tuple[float], a: float, b: float, c: float):
    """Calcular a distância de um ponto até uma reta ax + by + c = 0

    Args:
        point (tuple[float]): O ponto que quero calcular
        a (float): Coeficiente a
        b (float): Coeficiente b
        c (float): Coeficiente c
    """

    return abs(a*point[0]+b*point[1]+c)/math.sqrt(a**2+b**2)

def degrees_to_radians(angle: float|int):
    """Função que recebe um angulo em graus e retorna em radianos

    Args:
        angle (float | int): O ângulo a ser convertido
    """
    if not isinstance(angle, int) and not isinstance(angle, float):
        raise TypeError("Você não forneceu um tipo de ângulo válido")
    return (angle * math.pi)/180


def reduce_angle(angle: float|int):
    """Função que reduz o quadrante de um angulo em graus

    Args:
        angle (float | int): O Angulo que quero reduzir
    """
    if not isinstance(angle, int) and not isinstance(angle, float):
        raise TypeError('Você não passou um valor de angle válido')
    return angle % 360


def get_positive_angle(angle: float | int):
    """Se o ângulo for negativo, retorna o equivalente positivo

    Args:
        angle (float | int): Ângulo desejado
    """
    if not isinstance(angle, int) and not isinstance(angle, float):
        raise TypeError('Você não passou um valor de angle válido')
    return reduce_angle(angle) + 360 if angle < 0 else angle


def angle_between_vectors(vector1, vector2):
    norm_image_pointing = np.linalg.norm(vector1)
    norm_where_vector_will_go = np.linalg.norm(vector2)
    inner_product = np.dot(vector1, vector2)
    
    return radians_to_degrees(np.arccos(inner_product / (norm_image_pointing*norm_where_vector_will_go)))

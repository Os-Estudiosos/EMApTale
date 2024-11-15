import math

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

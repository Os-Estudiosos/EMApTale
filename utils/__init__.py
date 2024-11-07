
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

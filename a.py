import pygame
import math

# Inicializar o Pygame
pygame.init()

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gráfico de uma Função")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Função a ser desenhada (Exemplo: y = x^2)
def f(x):
    return math.sin(x)

# Escalas e deslocamentos
scale = 100  # Pixels por unidade
offset_x = width // 2  # Centro do eixo X
offset_y = height // 2  # Centro do eixo Y

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill(white)

    # Desenhar eixos
    pygame.draw.line(screen, black, (0, offset_y), (width, offset_y), 2)  # Eixo X
    pygame.draw.line(screen, black, (offset_x, 0), (offset_x, height), 2)  # Eixo Y

    # Desenhar o gráfico da função
    for x_pixel in range(0, width):
        # Converter pixel para coordenada no sistema cartesiano
        x = (x_pixel - offset_x) / scale
        y = f(x)

        # Converter coordenada cartesiana para pixel
        y_pixel = offset_y - y * scale

        # Desenhar ponto no gráfico (se estiver visível na tela)
        if 0 <= y_pixel < height:
            screen.set_at((x_pixel, int(y_pixel)), red)

    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()

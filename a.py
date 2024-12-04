import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configuração da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Retângulos com Alturas Variáveis")

# Cores
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Configuração dos retângulos
base_y = height - 50  # Base fixa para todos os retângulos
rect_width = 50
num_rectangles = 10

# Gerar retângulos e configurações de movimento
rectangles = []
speeds = []  # Velocidade de alteração da altura
for _ in range(num_rectangles):
    target_height = random.randint(50, 200)  # Altura inicial aleatória
    x = random.randint(0, width - rect_width)
    rectangles.append(pygame.Rect(x, base_y - target_height, rect_width, target_height))
    speeds.append(random.randint(1, 3))  # Velocidade de mudança aleatória

# Limites para as alturas
min_height = 50
max_height = 200

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill(WHITE)

    # Atualizar e desenhar os retângulos
    for i, rect in enumerate(rectangles):
        # Atualizar altura
        rect.height += speeds[i]
        rect.y -= speeds[i]  # Ajustar posição para manter a base fixa

        # Inverter a direção do crescimento ao atingir os limites
        if rect.height >= max_height or rect.height <= min_height:
            speeds[i] = -speeds[i]

        # Desenhar o retângulo
        pygame.draw.rect(screen, BLUE, rect)

    # Atualizar a tela
    pygame.display.flip()
    pygame.time.delay(30)  # Pequeno atraso para suavizar a animação

# Encerrar o Pygame
pygame.quit()

import pygame

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Definindo cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configurando o jogador como retângulo
player = pygame.Rect(50, 50, 30, 30)  # x, y, largura, altura
player_speed = 5

# Definindo uma parede poligonal
wall_points = [(300, 200), (500, 200), (550, 300), (400, 400), (250, 300)]

def point_in_polygon(point, poly_points):
    """Função para verificar se o ponto está dentro do polígono."""
    x, y = point
    n = len(poly_points)
    inside = False
    p1x, p1y = poly_points[0]
    for i in range(n + 1):
        p2x, p2y = poly_points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movendo o jogador
    keys = pygame.key.get_pressed()
    move_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    move_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

    # Movimento no eixo X e verificação de colisão
    player.x += move_x
    if point_in_polygon(player.center, wall_points):
        player.x -= move_x  # Desfaz movimento no eixo X se houver colisão

    # Movimento no eixo Y e verificação de colisão
    player.y += move_y
    if point_in_polygon(player.center, wall_points):
        player.y -= move_y  # Desfaz movimento no eixo Y se houver colisão

    # Desenho na tela
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player)  # Desenhar o jogador
    pygame.draw.polygon(screen, BLUE, wall_points)  # Desenhar a parede poligonal

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

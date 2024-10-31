import pygame
from classes.game import Game
from config import *

pygame.init()

def main():
    # Inicializando o Pygame
    game = Game(MEASURES, "EMApTale")
    running = True

    while running:
        # Checando os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.display.fill((0, 0, 0))

        # FAZER GAME AQUI
        


        # Atualizando
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()


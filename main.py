import pygame
from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager

from screens.menu import Menu

class Game:
    """Classe responsável pelo gerenciamento das partes mais internas do game, como volume,
    e outras opções, carregamento das informações e etc.
    """
    def __init__(self):
        pygame.init()

        # Colocando o tamanho da Tela
        self.display = pygame.display.set_mode(MEASURES)

        # Variável que indica se o jogo da rodando
        self.running = True

        # Colocando o nome da tela
        pygame.display.set_caption(GAME_NAME)

        # Criando o objeto do relógio
        self.clock = pygame.time.Clock()

        # Iniciando os Gerenciadores
        self.sound_manager = SoundManager()
        self.game_state_manager = GameStateManager('menu')

        # Definindo as cenas do jogo
        self.Menu = Menu('menu', self.display, self.sound_manager, self.game_state_manager)

        # Passando um Dicionário com meus cenários para o Gerenciador de Cenários
        self.game_state_manager.states = {
            'menu': self.Menu
        }

    def run(self):
        while self.running:
            # Checando os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            game.display.fill((0, 0, 0))

            # FAZER GAME AQUI
            
            self.game_state_manager.get_current_state().run()

            # Atualizando
            pygame.display.flip()

            # Limitando FPS
            self.clock.tick(FPS)
    
    def change_window_name(self, name: str):
        pygame.display.set_caption(name)


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()


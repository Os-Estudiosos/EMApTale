import pygame
from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager

# Importando minhas cenas
from screens.start import Start
from screens.combat import Combat

class Game:
    """Classe responsável pelo gerenciamento das partes mais internas do game, como volume,
    e outras opções, carregamento das informações e etc.
    """
    def __init__(self):
        # Colocando o tamanho da Tela
        self.display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.is_fullsize = False

        # Variável que indica se o jogo da rodando
        self.running = True

        # Colocando o nome da tela
        pygame.display.set_caption(GAME_NAME)

        # Criando o objeto do relógio
        self.clock = pygame.time.Clock()

        # Iniciando os Gerenciadores
        self.sound_manager = SoundManager()
        self.game_state_manager = GameStateManager('start')
        self.font_manager = FontManager()

        # Inicializando outras coisas
        self.sound_manager.load_all_sounds()  # Carregando todos os efeitos sonoros do jogo

        # Definindo as cenas do jogo
        self.Menu = Start('start', self.display, self.sound_manager, self.game_state_manager, self.font_manager)
        self.Combat = Combat('combat', self.display, self.sound_manager, self.game_state_manager, self.font_manager)

        # Passando um Dicionário com meus cenários para o Gerenciador de Cenários
        self.game_state_manager.states = {
            'start': self.Menu,
            'combat': self.Combat
        }

    def run(self):
        while self.running:
            # Checando os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_state_manager.set_state('start')
                    if event.key == pygame.K_2:
                        self.game_state_manager.set_state('combat')
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
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()


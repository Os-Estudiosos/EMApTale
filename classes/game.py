import pygame


class Game:
    """Classe responsável pelo gerenciamento das partes mais internas do game, como volume,
    e outras opções, carregamento das informações e etc.
    """
    def __init__(self, proportion: tuple[int], window_name: str = 'PYGAME'):
        self.display = pygame.display.set_mode(proportion)
        pygame.display.set_caption(window_name)
        self.clock = pygame.time.Clock()

    def limit_fps_to(self, fps: int):
        self.clock.tick(fps)
    
    def change_window_name(self, name: str):
        pygame.display.set_caption(name)

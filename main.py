import pygame
import os
import json

from config import *
from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.savemanager import SaveManager
from config.eventmanager import EventManager

from classes.player import Player

# Importando minhas cenas
from screens.menu.start import Start
from screens.menu.options import Options
from screens.menu.new_game import NewGameConfirmation
from screens.menu.new_name import NewName

from screens.combat import Combat
from screens.emap import EMAp
from screens.cutscene.intro_cutscene import IntroCutscene # Teste Brunão
from screens.show_day import ShowDay

from classes.text.text import Text

from screens.cutscene.gameover_cutscene import GameoverCutscene # Teste Brunão DOIS

class Game:
    """Classe responsável pelo gerenciamento das partes mais internas do game, como volume,
    e outras opções, carregamento das informações e etc.
    """
    def __init__(self):
        # Essa parte é apenas para a elaboração das coisas, vai ser removido depois
        # SaveManager.load()
        # Player.load_infos()
        
        # Colocando o tamanho da Tela
        self.display = pygame.display.set_mode((1280,720))
        #self.display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        # Variável que indica se o jogo da rodando
        self.running = True

        # Colocando o nome da tela
        pygame.display.set_caption(GAME_NAME)

        # Criando o objeto do relógio
        self.clock = pygame.time.Clock()

        # Inicializando outras coisas
        SoundManager.load_all_sounds()  # Carregando todos os efeitos sonoros do jogo

        # === Definindo as cenas do jogo ===
        # Cenas do Menu
        self.Menu = Start('start', self.display)
        self.NewGameConfirmation = NewGameConfirmation('new_game_confirmation', self.display)
        self.NewName = NewName('new_name', self.display)
        self.Options = Options('options', self.display)
        # Considereando em tirar o menu de opções (Não há muitas opções, só volume)

        # Cenas mais genéricas
        self.Combat = Combat('combat', self.display)
        self.EMAp = EMAp('emap', self.display)

        # Cena que mostra qual dia o player está
        self.ShowDay = ShowDay('show_day', self.display)

        # Cenas das Cutscenes
        self.IntroCutscene = IntroCutscene('intro_cutscene', self.display)
        self.GameoverCutscene = GameoverCutscene('gameover_cutscene', self.display)


        # Passando um Dicionário com meus cenários para o Gerenciador de Cenários
        GameStateManager.states = {
            # Cenas do menu
            'start': self.Menu,
            'new_game_confirmation': self.NewGameConfirmation,
            'new_name': self.NewName,
            'options': self.Options,

            # Cenas das Cutscenes
            'intro_cutscene': self.IntroCutscene,
            'gameover_cutscene': self.GameoverCutscene,

            # Cenas genéricas
            'combat': self.Combat,
            'emap': self.EMAp,
            'show_day': self.ShowDay
        }

        pygame.mouse.set_visible(False)

    def handle_events(self):
        # Checando os eventos
        EventManager.events = pygame.event.get()
        for event in EventManager.events:
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handle_events()

            game.display.fill((0, 0, 0))

            # Trocando de Cena
            GameStateManager.get_current_state().run()

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


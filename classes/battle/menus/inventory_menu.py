import pygame

from config.fontmanager import FontManager

from classes.battle.menus import BattleMenu

from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.player import Player
from classes.text.text import Text

class InventoryMenu(BattleMenu):
    def __init__(self, battle_container):
        self.__options: list[Text] = []  # Lista de opções
        self.container = battle_container  # Container dos menus
        self.display = pygame.display.get_surface()  # A tela do jogo

        # Adicionando os itens como minhas opções
        for item in Player.inventory:
            self.__options.append(Text(item.name, FontManager.fonts['Gamer'], 40))
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_x] or keys[pygame.K_BACKSPACE]:  # Para eu voltar no menu anterior
            BattleMenuManager.go_back()
    
    def draw(self):
        for opt in self.__options:
            opt.draw(self.display)
    
    @property
    def options(self):
        return self.__options

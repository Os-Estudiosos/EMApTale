import pygame 
from .history_cutscene import HistoryCutscene

class CutsceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.cutscenes = {
            "history": HistoryCutscene(screen),
        } 
        self.active_cutscene = None

    def play_cutscene(self, name):
        """Inicia a Cutscene com base no nome
        """
        if name in self.cutscenes:
            self.active_cutscene = self.cutscenes[name]
            self.active_cutscene.play()

    def update(self):
        if self.active_cutscene:
            self.active_cutscene.update()
            if self.active_cutscene.is_finished():
                self.active_cutscene = none

    
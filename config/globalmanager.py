import os
import json

from config import *
from config.savemanager import SaveManager


class GlobalManager:
    """Função que carrega a maioria das informações úteis do jogo, como a lista de interações, o dia que o jogo está rodando e etc."""
    interactions = []
    day = None
    bosses = {}
    items = {}

    @classmethod
    def load_infos(cls):
        cls.day = SaveManager.loaded_save['day']  # Carregando o dia atual

        with open(os.path.join(GET_PROJECT_PATH(), 'infos', 'items.json')) as file:
            cls.items = json.loads(file)
        
        with open(os.path.join(GET_PROJECT_PATH(), 'infos', 'boss.json')) as file:
            cls.bosses = json.loads(file)

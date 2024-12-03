import os
import json

from config import *
from config.savemanager import SaveManager

from classes.map.camera import Camera


class GlobalManager:
    """Função que carrega a maioria das informações úteis do jogo, como a lista de interações, o dia que o jogo está rodando e etc."""
    interactions = []
    day = None
    bosses = {}
    items = []
    groups = {}
    camera: Camera = None
    paused = False
    on_inventory = False
    spawnpoint = [0,0]

    @classmethod
    def pass_day(cls):
        cls.day += 1

    @classmethod
    def pause(cls):
        cls.paused = True
    
    @classmethod
    def resume(cls):
        cls.paused = False

    @classmethod
    def set_camera(cls, camera_instance):
        cls.camera = camera_instance

    @classmethod
    def load_infos(cls):
        cls.day = SaveManager.loaded_save['day']  # Carregando o dia atual

        with open(os.path.join(GET_PROJECT_PATH(), 'infos', 'items.json')) as file:
            cls.items = json.load(file)
        
        with open(os.path.join(GET_PROJECT_PATH(), 'infos', 'boss.json')) as file:
            cls.bosses = json.load(file)
    
    @classmethod
    def get_item(cls, item_id):
        for item in cls.items:
            if item['id_item'] == item_id:
                return item

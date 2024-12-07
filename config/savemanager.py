import os
import platform
from pathlib import Path
import json

from classes.player import Player
from config.globalmanager import GlobalManager


class SaveManager:
    home = Path.home()
    platform = platform.system()
    loaded_save = {}
    default_save_information = {
        "name": "",
        "day": 1,
        "inventory": [
            {
                "item_id": "pencil",
                "scale": 1,
                "sprite": "pencil.png",
                "name": "Lápis",
                "type": "weapon",
                "damage": 5,
                "description": "É o que eu tinha na mochila",
                "equiped": True
            },
        ],
        "player": {
            "life": 20,
            "max_life": 20,
            "actual_xp": 0,
            "max_xp": 100,
            "level": 1,
            "map_position": None
        }
    }

    @classmethod
    def create_save_folder_path(cls, pth) -> None:
        os.mkdir(pth)

    @classmethod
    def get_save_folder_path(cls) -> str:
        if cls.platform == 'Linux':
            general_path = os.path.join(cls.home, '.local', 'share', 'emaptale')

            if os.path.exists(general_path):
                return general_path
            else:
                cls.create_save_folder_path(general_path)
                return cls.get_save_folder_path()
        if cls.platform == 'Windows':
            general_path = os.path.join(cls.home, 'AppData', 'Roaming', 'emaptale')

            if os.path.exists(general_path):
                return general_path
            else:
                cls.create_save_folder_path(general_path)
                return cls.get_save_folder_path()

    @classmethod
    def load(cls):
        """Função que carrega um arquivo de save e coloca as devidas variáveis nos locais corretos

        Args:
            slot (int): Qual dos arquivos vão ser carregados (0 a 3)
        """
        save_path = cls.get_save_folder_path()

        with open(os.path.join(save_path, f'save_file.json'), 'r') as save_file:
            cls.loaded_save = json.load(save_file)
    
    @classmethod
    def create_new_save_file(cls, player_name):
        with open(os.path.join(cls.get_save_folder_path(), 'save_file.json'), 'w') as file:
            cls.default_save_information['name'] = player_name
            file.write(json.dumps(cls.default_save_information, indent=4))
    
    @classmethod
    def save(cls):
        folder_path = cls.get_save_folder_path()

        if not cls.save_exists():  # Levantando erro caso use de forma errada
            raise FileNotFoundError("Não podemos salvar o jogo sem que haja um arquivo de save")
        
        new_information = cls.loaded_save.copy()

        new_information['player']['life'] = Player.life
        new_information['player']['max_life'] = Player.max_life
        new_information['player']['map_position'] = Player.map_position

        new_information['inventory'] = Player.inventory.get_dict()

        new_information['day'] = GlobalManager.day

        with open(os.path.join(folder_path, 'save_file.json'), 'w') as file:
            file.write(json.dumps(new_information, indent=4))
    
    @classmethod
    def save_exists(cls) -> bool:
        folder_path = cls.get_save_folder_path()
        return os.path.exists(os.path.join(folder_path, 'save_file.json'))

import os
import platform
from pathlib import Path
import json


class SaveManager:
    home = Path.home()
    platform = platform.system()
    loaded_save = {}
    default_save_information = {
        "name": "",
        "day": 1,
        "equiped_item": 0,
        "inventory": [
            {
                'id': 'pencil',
                "name": "Lápis",
                "type": "weapon",
                "damage": 5,
                "description": "É o que eu tinha na mochila",
                "equiped": True
            }
        ],
        "player": {
            "life": 20,
            "max_life": 20,
            "actual_xp": 0,
            "max_xp": 100,
            "level": 1
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
        raise NotImplementedError
    
    @classmethod
    def save_exists(cls) -> bool:
        folder_path = cls.get_save_folder_path()
        return os.path.exists(os.path.join(folder_path, 'save_file.json'))

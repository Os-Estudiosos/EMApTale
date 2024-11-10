import os
import platform
from pathlib import Path
import json


class SaveManager:
    home = Path.home()
    platform = platform.system()
    loaded_save = {}

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

        try:
            with open(os.path.join(save_path, f'save_file.json'), 'r') as save_file:
                cls.loaded_save = json.load(save_file)
        except FileNotFoundError as err:
            raise FileNotFoundError("Este erro não deveria acontecer, pois o player conseguiu pedir um slot que não existe") from err
    
    @classmethod
    def save(cls):
        raise NotImplementedError
    
    @classmethod
    def save_exists(cls) -> bool:
        folder_path = cls.get_save_folder_path()
        return os.path.exists(os.path.join(folder_path, 'save_file.json'))

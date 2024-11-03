import os
import platform
from pathlib import Path


class SaveManager:
    home = Path.home()
    platform = platform.system()

    @classmethod
    def create_save_folder_path(cls, pth):
        os.mkdir(pth)

    @classmethod
    def get_save_folder_path(cls):
        general_path = os.path.join(cls.home, '.local', 'share', 'emaptale')

        if cls.platform == 'Linux':
            if os.path.exists(general_path):
                return general_path
            else:
                cls.create_save_folder_path(general_path)
                return cls.get_save_folder_path()

    # @classmethod
    # def load(cls, slot: int):
        

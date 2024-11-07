import unittest
import os
import sys
import pathlib
import platform
sys.path.append(os.path.join(os.getcwd()))

from config.savemanager import SaveManager


class SaveManagerTests(unittest.TestCase):
    actual_platform = platform.system()

    def test_getting_folder_path(self):
        """Testando se a função está retornando a pasta dos saves
        """
        if self.actual_platform == 'Linux':
            self.assertEqual(
                SaveManager.get_save_folder_path(),
                os.path.join(pathlib.Path.home(), '.local', 'share', 'emaptale')
            )
        if self.actual_platform == 'Windows':
            self.assertEqual(
                SaveManager.get_save_folder_path(),
                os.path.join(pathlib.Path.home(), 'AppData', 'Roaming', 'emaptale')
            )
    
    def test_loading_slot(self):
        """Testando se as informações estão sendo carregadas
        """

        game_dict_key_types = {
            'name': str,
            'day': int,
            'inventory': list,
            'player': dict
        }

        SaveManager.load()
        for k, v in SaveManager.loaded_save.items():
            self.assertIn(k, game_dict_key_types)
            self.assertIsInstance(v, game_dict_key_types[k])

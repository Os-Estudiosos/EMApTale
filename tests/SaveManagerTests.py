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
            'day': int,
            'inventory': list,
            'player_pos': list
        }

        saves_que_vao_retornar_algo = []

        if self.actual_platform == 'Linux':
            for save_file in os.scandir(os.path.join(pathlib.Path.home(), '.local', 'share', 'emaptale')):
                saves_que_vao_retornar_algo.append(save_file.name)
        if self.actual_platform == 'Windows':
            for save_file in os.scandir(os.path.join(pathlib.Path.home(), 'AppData', 'Roaming', 'emaptale')):
                saves_que_vao_retornar_algo.append(save_file.name)
        

        for i in range(4):
            if f'save_game_{i}.json' not in saves_que_vao_retornar_algo:
                self.assertRaises(FileNotFoundError, SaveManager.load, i)
                continue

            SaveManager.load(i)
            for k, v in SaveManager.loaded_save.items():
                self.assertIn(k, game_dict_key_types)
                self.assertIsInstance(v, game_dict_key_types[k])

import unittest
import os
import sys
import pathlib
import platform
sys.path.append(os.path.join(os.getcwd()))

from config.savemanager import SaveManager


class SaveManagerTests(unittest.TestCase):
    def test_getting_folder_path(self):
        actual_platform = platform.system()

        if actual_platform == 'Linux':
            self.assertEqual(
                SaveManager.get_save_folder_path(),
                os.path.join(pathlib.Path.home(), '.local', 'share', 'emaptale')
            )

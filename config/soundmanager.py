import pygame
import os
from config import GET_PROJECT_PATH


class SoundManager:
    def __init__(self):
        self.audios: dict[str, pygame.mixer.Sound] = {
        }  # Dicionários dos sons carregados

        self.__volume = 1  # Volume geral (Todo som vai ter o mesmo volume)
    
    def play_music(self, file, loop: int = 0, start: int = 0, fade_ms: int = 0):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loop, start, fade_ms)
    
    def unload_music(self):
        pygame.mixer.music.unload()
    
    def load_all_sounds(self):
        # for sound in scan_
        base_path = os.path.join(GET_PROJECT_PATH(), 'sounds')
        for sound in os.scandir(base_path):
            self.audios[sound.name] = pygame.mixer.Sound(os.path.join(base_path, sound.name))
    
    def unload_sounds(self):
        for key in self.audios.keys():
            del self.audios[key]
    
    def play_sound(self, sound_name):
        self.audios[sound_name].play()
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def resume_music(self):
        pygame.mixer.music.unpause()
    

    @property
    def volume(self):  # Getter do meu volume
        return self.__volume

    @volume.setter
    def volume(self, vol):  # Setter do meu volume
        if not 0<=vol<=1:
            raise ValueError("Você precisa fornecer um número entre 0 e 1")
        self.__volume = vol
        pygame.mixer.music.set_volume(self.__volume)

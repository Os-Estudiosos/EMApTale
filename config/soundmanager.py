import pygame


class SoundManager:
    def __init__(self):
        self.music = []  # Músicas que estão ou serão tocadas
        self.audios = []  # Áudios que estão ou serão tocados

        self.__volume = 1  # Volume geral (Todo som vai ter o mesmo volume)
    
    def add_music(self, file):
        self.music.append(file)
    
    def play_queued_music(self, loop: int = 0, start: int = 0, fade_ms: int = 0):
        pygame.mixer.music.load(self.music[0])
        pygame.mixer.music.play(loop, start, fade_ms)
        self.music.pop(0)
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def resume(self):
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

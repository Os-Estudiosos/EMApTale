import pygame
from abc import ABC, abstractmethod
from config.soundmanager import SoundManager


class Boss(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def take_damage(self, amount: float):...

    @abstractmethod
    def speak(self, text: str):...

    @abstractmethod
    def choose_attack(self):...

    @abstractmethod
    def draw(self, screen: pygame.Surface):...
    
    def apply_effect(self, effect):
        if effect == '-defense':
            self.defense = 0
    
    def take_damage(self, amount):
        self.life = self.life - amount*amount/(amount+self.defense)
        SoundManager.play_sound('damage.wav')
        if self.life <= 0:
            self.life = 0
            self.dead = True
        self.state = 'shaking'
        self.counter = 0
    
    @property
    @abstractmethod
    def counter(self):...

    @counter.setter
    @abstractmethod
    def counter(self, value):...

    @property
    @abstractmethod
    def state(self):...

    @state.setter
    @abstractmethod
    def state(self, value):...

    @property
    @abstractmethod
    def dead(self):...

    @dead.setter
    @abstractmethod
    def dead(self, value):...

    @property
    @abstractmethod
    def voice(self):...

    @voice.setter
    @abstractmethod
    def voice(self, value):...

    @property
    @abstractmethod
    def life(self):...

    @life.setter
    @abstractmethod
    def life(self, value):...

    @property
    @abstractmethod
    def max_life(self):...

    @max_life.setter
    @abstractmethod
    def max_life(self, value):...

    @property
    @abstractmethod
    def defense(self):...

    @defense.setter
    @abstractmethod
    def defense(self, value):...

    @property
    @abstractmethod
    def damage(self):...

    @damage.setter
    @abstractmethod
    def damage(self, value):...


class Attack(ABC):
    @property
    @abstractmethod
    def player(self):...

    @property
    @abstractmethod
    def duration(self):...

    @property
    @abstractmethod
    def duration_counter(self):...

    @abstractmethod
    def run(self):...

    @abstractmethod
    def restart(self):...


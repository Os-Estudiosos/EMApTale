from abc import ABC, abstractmethod
import pygame


class Boss(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def take_damage(self, amount: float):...

    @abstractmethod
    def speak(self, text: str):...

    @abstractmethod
    def choose_attack(self):...

    @abstractmethod
    def draw(self, screen: pygame.Surface):...

    @abstractmethod
    def apply_effect(self, effect):...

    @property
    @abstractmethod
    def voice(self):...

    @property
    @abstractmethod
    def life(self):...

    @property
    @abstractmethod
    def max_life(self):...

    @property
    @abstractmethod
    def defense(self):...

    @property
    @abstractmethod
    def damage(self):...

    @property
    @abstractmethod
    def music(self):...


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


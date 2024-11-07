from abc import ABC, abstractmethod


class BattleMenu(ABC):
    @property
    @abstractmethod
    def options(self):...
    
    @abstractmethod
    def draw(self):...

    @abstractmethod
    def update(self):...

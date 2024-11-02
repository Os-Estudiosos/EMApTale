from abc import ABC, abstractmethod


class State(ABC):
    """Classe Imaginária que descreve tudo que uma Cena deve ter
    """

    @property
    @abstractmethod
    def display(self):...

    @property
    @abstractmethod
    def sound_manager(self):...

    @property
    @abstractmethod
    def game_state_manager(self):...

    @property
    @abstractmethod
    def font_manager(self):...

    @property
    @abstractmethod
    def name(self):...

    @property
    @abstractmethod
    def execution_counter(self):...

    @abstractmethod
    def run(self):...

    @abstractmethod
    def on_first_execution(self):...

    @abstractmethod
    def on_last_execution(self):...

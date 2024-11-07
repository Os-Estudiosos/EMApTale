from abc import ABC, abstractmethod


class State(ABC):
    """Classe Imaginária que descreve tudo que uma Cena deve ter

    Ciclo de Vida de uma Cena:
    - Toda cena tem um código que é executado assim que ela é inicializada (__init__)
    - Toda cena também possui um código que é executado apenas uma vez no início quando ela é "renderizada" na tela (on_first_execution)
    - Toda cena tem o código que roda a cada quadro do jogo (run)
    - Toda cena tem um código que roda assim que ela é trocada por outra cena (on_last_execution)
    """

    @property
    @abstractmethod
    def display(self):
        """Toda cena deve ter um atributo DISPLAY que recebe a tela principal do jogo"""

    @property
    @abstractmethod
    def game_state_manager(self):
        """Toda cena deve ter o gerenciador de cenas caso queiram mudar dinamicamente"""

    @property
    @abstractmethod
    def name(self):
        """Toda cena deve seu nome"""
    
    @property
    @abstractmethod
    def variables(self):
        """Toda cena deve ter variáveis que são passadas dinamicamente pelo game state manager"""
    
    @variables.setter
    @abstractmethod
    def variables(self):
        """É obrigatório ter o método setter das variáveis"""

    @property
    @abstractmethod
    def execution_counter(self):
        """Propriedade auxiliar, utilizada para contabilizar se o método "on_first_execution" deve ser executado"""

    @abstractmethod
    def run(self):
        """Código que roda a cada quadro do jogo"""

    @abstractmethod
    def on_first_execution(self):
        """Código que é executado apenas uma vez no início quando ela é "renderizada" na tela"""

    @abstractmethod
    def on_last_execution(self):
        """Código que roda assim que ela é trocada por outra cena"""

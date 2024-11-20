from screens import State


class GameStateManager:
    """Classe que gerencia qual a Cena do game está aparecendo
    """
    def __init__(self, initial_state):
        self.states: dict[str, State] = {}  # Dicionário de todos os cenários
        self.current_state = initial_state  # Cenário que está rodando agora
    
    def get_current_state_name(self) -> str:
        """Pega o nome do cenário que está rodando atualmente

        Returns:
            str: Nome do Cenário atual
        """
        return self.current_state
    
    def get_current_state(self) -> State:
        """Retorna o cenário atual (Objeto)

        Returns:
            State: Cenário que está rodando agora
        """
        return self.states[self.current_state]

    def set_state(self, current_state: str, variables: dict = {}) -> None:
        """Função que altera o cenário atual de acordo com o nome que eu passar

        Args:
            current_state (str): Nome do cenário que eu quero rodar
            variables (dict): Dicionário com variáveis que vão ser passadas para a cena

        Raises:
            KeyError: Levanto se o parametro passado não está dentro das chaves do dicionário com todos os cenários carregados
        """
        if current_state not in self.states.keys():
            raise KeyError('Você forneceu um nome de cenário que não está no dicionário geral')
        self.get_current_state().on_last_execution()
        self.current_state = current_state
        self.get_current_state().variables = variables


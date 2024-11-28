from screens import State

class GameStateManager:
    """Classe que gerencia qual a Cena do game está aparecendo
    """
    states: dict[str, State] = {}  # Dicionário de todos os cenários
    current_state = 'start'  # Cenário que está rodando agora
    previous_state = None
    
    @classmethod
    def get_current_state_name(cls) -> str:
        """Pega o nome do cenário que está rodando atualmente

        Returns:
            str: Nome do Cenário atual
        """
        return cls.current_state
    
    @classmethod
    def get_current_state(cls) -> State:
        """Retorna o cenário atual (Objeto)

        Returns:
            State: Cenário que está rodando agora
        """
        return cls.states[cls.current_state]

    @classmethod
    def go_back(cls):
        cls.set_state(cls.previous_state)

    @classmethod
    def set_state(cls, current_state: str, variables: dict = {}) -> None:
        """Função que altera o cenário atual de acordo com o nome que eu passar

        Args:
            current_state (str): Nome do cenário que eu quero rodar
            variables (dict): Dicionário com variáveis que vão ser passadas para a cena

        Raises:
            KeyError: Levanto se o parametro passado não está dentro das chaves do dicionário com todos os cenários carregados
        """
        if current_state not in cls.states.keys():
            raise KeyError('Você forneceu um nome de cenário que não está no dicionário geral')
        cls.get_current_state().on_last_execution()
        cls.previous_state =  cls.current_state
        cls.current_state = current_state
        cls.get_current_state().variables = variables


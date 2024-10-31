from screens import State

class GameStateManager:
    """Classe que gerencia qual a Cena do game está aparecendo
    """
    def __init__(self, initial_state):
        self.states = {}
        self.current_state = initial_state
    
    def get_current_state_name(self) -> str:
        return self.current_state
    
    def get_current_state(self) -> State:
        return self.states[self.current_state]

    def set_state(self, current_state) -> None:
        self.current_state = current_state


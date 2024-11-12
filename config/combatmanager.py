

class CombatManager:
    turn = 'player'

    @classmethod
    def set_player_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'player'
    
    @classmethod
    def set_boss_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'boss'

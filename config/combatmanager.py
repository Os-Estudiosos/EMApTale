from classes.bosses.yuri import Yuri

class CombatManager:
    turn = 'player'
    enemy = None

    @classmethod
    def set_player_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'player'
    
    @classmethod
    def set_boss_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'boss'
    
    @classmethod
    def set_boss(cls, infos: dict, variables: dict):
        """Método que inicializa o meu inimigo do combate

        Args:
            infos (dict): Dicionário com as informações do Boss
        """

        if infos['name'] == 'Yuri Saporito':
            cls.enemy = Yuri(infos, **variables)

import pygame


class CombatManager:
    turn = 'player'
    enemy = None
    global_variables = {  # Variáveis globais
        'player': None,
        'player_group': None,
        'battle_container': None
    }

    global_groups: list[pygame.sprite.Group] = []  # Alguns objetos tem que ser desenhados em cima de todo o resto, pra isso criei essa variável

    @classmethod
    def set_player_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'player'
    
    @classmethod
    def set_boss_turn(cls):
        """Método que coloca como turno do player"""
        cls.turn = 'boss'
    
    @classmethod
    def set_boss(cls, infos: dict):
        """Método que inicializa o meu inimigo do combate

        Args:
            infos (dict): Dicionário com as informações do Boss
        """
        from classes.bosses.yuri import Yuri

        if infos['name'] == 'Yuri Saporito':
            cls.enemy = Yuri(infos)
    
    @classmethod
    def set_variable(cls, key: str, value):
        """Método que altera uma variável global

        Args:
            key (str): Chave que vai ser alterada do dicionário
            value (Any): O valor a ser armazenado
        """
        cls.global_variables[key] = value
    
    @classmethod
    def get_variable(cls, key: str):
        """Retorna a variável pedida

        Args:
            key (str): A chave da variável global
        
        Returns:
            (Any): A variável pedida
        """
        return cls.global_variables[key]
    
    @classmethod
    def draw_global_groups(cls, screen):
        for group in cls.global_groups:
            group.draw(screen)
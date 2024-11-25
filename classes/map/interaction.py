import pygame

class InteractionManager:
    def __init__(self, interactions, player):
        """
        Gerencia as interações do jogador com objetos do mapa.
        :param interactions: Lista de objetos de interação carregados do mapa.
        :param player: Referência ao jogador (para posição).
        """
        self.interactions = interactions
        self.player = player
        self.active_interaction = None
        self.interaction_in_progress = False  # Para manter interações

    def check_interaction(self, events):
        """
        Verifica se o jogador está próximo de um objeto de interação.
        :param events: Lista de eventos do Pygame.
        :return: Objeto de interação ativo (se houver).
        """
        player_rect = self.player.rect
        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])

            # Jogador está na área de interação
            if player_rect.colliderect(rect):
                self.active_interaction = interaction
                return interaction

        # Se o jogador saiu de todas as áreas de interação
        self.active_interaction = None
        return None

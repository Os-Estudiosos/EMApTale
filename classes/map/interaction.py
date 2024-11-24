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
        self.interaction_triggered = False  # Para interações únicas
        self.interaction_in_progress = False  # Para manter interações

    def draw(self, screen, camera):
        """
        Desenha as áreas de interação como retângulos.
        :param screen: Tela principal do Pygame.
        :param camera: Gerenciador da câmera.
        """
        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(rect), 2)  # Vermelho para destacar

    def check_interaction(self, events):
        """
        Verifica se o jogador está próximo de um objeto de interação.
        :param events: Lista de eventos do Pygame.
        :return: Objeto de interação ativo (se houver).
        """
        player_rect = self.player.rect
        interaction_found = False

        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])

            if player_rect.colliderect(rect):  # Jogador está na área de interação
                interaction_found = True
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:  # Pressionar "Z" inicia
                        self.active_interaction = interaction
                        self.interaction_in_progress = True  # Inicia interação
                        return interaction

        # Se não há interação ativa e o jogador saiu da área
        if not interaction_found:
            self.active_interaction = None
            self.interaction_in_progress = False

        return None

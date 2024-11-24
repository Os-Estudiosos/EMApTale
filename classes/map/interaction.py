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

    def draw(self, screen, camera):
        """
        Desenha as áreas de interação como retângulos.
        :param screen: Tela principal do Pygame.
        :param camera: Gerenciador da câmera.
        """
        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(rect), 2)  # Vermelho para destacar

    def check_interaction(self, keys):
        """
        Verifica se o jogador está próximo de um objeto de interação.
        :param keys: Teclas pressionadas pelo jogador.
        :return: Objeto de interação ativo (se houver).
        """
        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])
            player_rect = self.player.rect
            if player_rect.colliderect(rect):  # Verifica proximidade
                if keys[pygame.K_e]:  # Verifica tecla "E"
                    print(f"Interação ativada: {interaction['interaction_name']}")
                    print(f"Mensagem: {interaction['value']}")
                    self.active_interaction = interaction
                    return interaction

        self.active_interaction = None  # Nenhuma interação ativa
        return None

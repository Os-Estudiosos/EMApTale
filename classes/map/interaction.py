import pygame
import os
from config import *
from classes.text.dynamic_text import DynamicText
from config.eventmanager import EventManager
from config.globalmanager import GlobalManager
from config.gamestatemanager import GameStateManager
from config.savemanager import SaveManager


class Interaction:
    def __init__(self, **kwargs):
        self.rect = pygame.Rect(kwargs['x'], kwargs['y'], kwargs['width'], kwargs['height'])
        self.interaction_name = kwargs['interaction_name']
        self.value = kwargs['value']
        self.day = kwargs['day']
    

class BossIntercation(Interaction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boss = kwargs['boss']
    
    def go_to_boss_fight(self):
        SaveManager.save()
        GameStateManager.set_state('combat', {
            "enemy": GlobalManager.bosses[self.boss]
        })


class CamachoInteraction(Interaction):
    def go_to_camacho(self):
        GameStateManager.set_state('final_cutscene')


class InteractionManager:
    def __init__(self, player, chatbox, tecla_z_image):
        """
        Gerencia as interações do jogador com objetos do mapa.
        :param interactions: Lista de objetos de interação carregados do mapa.
        :param player: Referência ao jogador (para posição).
        :param chatbox: Imagem da caixa de texto.
        :param tecla_z_image: Imagem da tecla "Z" para exibir quando na área de interação.
        """
        self.player = player
        self.active_interaction = None
        self.interaction_in_progress = False  # Para manter interações
        self.dynamic_text = None  # Controla o texto dinâmico da interação
        self.chatbox = chatbox
        self.tecla_z_image = tecla_z_image
        self.chatbox_position = None  # Será configurada na inicialização

    def set_chatbox_position(self, position):
        """
        Define a posição da caixa de texto.
        :param position: Posição da caixa de texto.
        """
        self.chatbox_position = position

    def check_interaction(self):
        """
        Verifica se o jogador está próximo de um objeto de interação.
        :param events: Lista de eventos do Pygame.
        :return: Objeto de interação ativo (se houver).
        """
        for interaction in GlobalManager.interactions:
            # Jogador está na área de interação
            if (
                (interaction.rect.colliderect(self.player.rect))
                    and
                (
                    interaction.day == None
                    or
                    interaction.day == GlobalManager.day
                )
            ):
                self.active_interaction = interaction
                return interaction

        # Se o jogador saiu de todas as áreas de interação
        self.active_interaction = None
        return None

    def handle_interaction(self):
        """
        Gerencia a lógica de interações, incluindo exibição de textos dinâmicos.
        :param events: Lista de eventos do Pygame.
        """
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and (not GlobalManager.on_inventory and not GlobalManager.paused):
                    # Inicia ou encerra interações
                    if self.dynamic_text:
                        if self.dynamic_text.finished:
                            # Encerra a interação
                            if isinstance(self.active_interaction, BossIntercation):
                                self.active_interaction.go_to_boss_fight()
                            if isinstance(self.active_interaction, CamachoInteraction):
                                self.active_interaction.go_to_camacho()
                            self.dynamic_text = None
                            self.active_interaction = None
                        else:
                            self.dynamic_text.skip_text()
                    elif self.active_interaction:
                        # Inicia interação com texto dinâmico
                        self.dynamic_text = DynamicText(
                            text=f"{self.active_interaction.value}",
                            font="fonts/Gamer.ttf",
                            letters_per_second=20,
                            text_size=70,
                            position=(
                                self.chatbox_position[0] + 20,  # Margem lateral
                                self.chatbox_position[1] + 20  # Margem superior
                            ),
                            color=(255, 255, 255),
                            max_length=self.chatbox.get_width() - 40,
                            sound='text_1.wav'
                        )

    def render_interaction(self, display):
        """
        Renderiza elementos da interação (tecla "Z", caixa de texto, texto dinâmico).
        :param display: Superfície principal do Pygame.
        """
        # Exibe a tecla "Z" se o jogador estiver na área de interação
        if self.active_interaction and not self.dynamic_text:
            key_rect = self.tecla_z_image.get_rect(center=self.player.rect.center)
            key_rect.bottom = self.player.rect.top - 20
            display.blit(self.tecla_z_image, GlobalManager.camera.apply(key_rect))

        # Renderiza a caixa de texto e o texto dinâmico
        if self.dynamic_text:
            display.blit(self.chatbox, self.chatbox_position)
            self.dynamic_text.update()
            self.dynamic_text.draw(display)

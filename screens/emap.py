import pygame
import os

from screens import State

from config import *
from config.savemanager import SaveManager
from config.globalmanager import GlobalManager
from config.eventmanager import EventManager
from config.gamestatemanager import GameStateManager
from config.soundmanager import SoundManager

from classes.map.interaction import InteractionManager
from classes.map.loader import MapLoader
from classes.map.camera import Camera
from classes.frisk import Frisk
from classes.player import Player
from classes.map.infos_hud import InfosHud

from screens.subscreen.pause_menu import PauseMenu

class EMAp(State):
    def __init__(self, name, display):
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display
        self.__execution_counter = 0

        self.items_group = pygame.sprite.Group()
        GlobalManager.groups['items'] = self.items_group

        # Inicializa o loader do mapa
        self.map_loader = MapLoader(os.path.join(GET_PROJECT_PATH(), 'tileset', 'emap.tmx'))
        self.map_loaded = False

        self.map_loader.load_items()
        self.map_loader.load_walls()  # Carrega as áreas de colisão do mapa
        self.map_loader.load_interactions()

        # Configura a câmera com as dimensões do mapa e da tela
        map_width, map_height = self.map_loader.get_size()
        screen_width, screen_height = self.__display.get_size()
        self.camera = Camera(map_width, map_height, screen_width, screen_height)
        GlobalManager.set_camera(self.camera)

        # Inicializa o jogador
        self.player = Frisk(self.map_loader.walls)

        # Inicializa o InteractionManager
        chatbox = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'chatbox.png'))
        tecla_z_image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'tecla_z.png'))
        self.tecla_f_image = pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'tecla_f.png'))

        # Redimensiona a chatbox
        new_width = chatbox.get_width() + 1100  # Ajuste personalizado
        new_height = chatbox.get_height() + 250
        chatbox = pygame.transform.scale(chatbox, (new_width, new_height))

        # Redimensiona a imagem da tecla "Z"
        tecla_z_image = pygame.transform.scale_by(tecla_z_image, 0.9)
        self.tecla_f_image = pygame.transform.scale_by(self.tecla_f_image, 0.9)

        # Inicializa o InteractionManager
        self.interaction_manager = InteractionManager(
            self.player, chatbox, tecla_z_image
        )
        self.interaction_manager.set_chatbox_position((
            (self.__display.get_width() - new_width) // 2,  # Centraliza horizontalmente
            self.__display.get_height() - new_height        # Posiciona no rodapé
        ))

        self.pause_menu = PauseMenu('pause_menu', self.__display)

        GlobalManager.on_inventory = False
        self.infos_hud: InfosHud = None

    def on_first_execution(self):
        self.player.reset_position()
        SaveManager.load()
        GlobalManager.load_infos()
        SoundManager.stop_music()
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "map_audio.wav"))
        self.camera.empty()
        self.items_group.empty()
        self.player.load_infos()
        self.map_loader = MapLoader(os.path.join(GET_PROJECT_PATH(), 'tileset', 'emap.tmx'))
        self.map_loader.load_items()
        self.map_loader.load_walls()  # Carrega as áreas de colisão do mapa
        self.map_loader.load_interactions()
        self.map_loaded = True
        self.infos_hud = InfosHud(self.items_group)

        if Player.previous_map_position and GameStateManager.previous_state == 'start':
            self.player.reset_position(Player.previous_map_position)
        elif GameStateManager.previous_state == 'show_day':
            self.player.reset_position()
            GlobalManager.pass_day()
            SaveManager.save()

        GlobalManager.paused = False

    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
        
        keys = pygame.key.get_pressed()

        # Limpa a tela
        self.__display.fill((0, 0, 0))

        # Atualiza a posição da câmera para seguir o jogador
        self.camera.update(self.player.rect)

        # Renderiza os tiles do mapa
        self.map_loader.render_with_vector(self.__display, self.camera)

        # Coleta e ordena os objetos renderizáveis (incluindo o jogador)
        renderables = self.map_loader.get_renderables(self.player)
        renderables = self.camera.apply_ysort(renderables)


        # Renderiza os objetos na ordem correta
        for _, image, rect in renderables:
            if isinstance(image, pygame.Surface):
                self.__display.blit(image, rect)
            elif isinstance(image, Frisk):
                image.draw(self.__display)
    
        self.camera.draw(self.__display)

        # Captura eventos e gerencia interações
        self.interaction_manager.handle_interaction()
        self.interaction_manager.render_interaction(self.__display)

        item_collided = pygame.sprite.spritecollide(self.player, self.items_group, False, pygame.sprite.collide_mask)

        if item_collided:
            key_rect = self.tecla_f_image.get_rect(center=self.player.rect.center)
            key_rect.bottom = self.player.rect.top - 20
            self.__display.blit(self.tecla_f_image, self.camera.apply(key_rect))

        # Checando se pausou
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GlobalManager.paused = not GlobalManager.paused
                if event.key == pygame.K_f and item_collided:
                    self.player.inventory.add_item(item_collided[0])
                    item_collided[0].kill()
                    self.infos_hud.update_infos()
                if event.key == pygame.K_e:
                    GlobalManager.on_inventory = not GlobalManager.on_inventory

        # ====== UPDATES DO CENÁRIO =====
        # Se o jogo não estiver pausado nem estiver no inventário
        if not GlobalManager.paused and not GlobalManager.on_inventory:
            self.interaction_manager.check_interaction()
            self.items_group.update()
            if not self.interaction_manager.dynamic_text:
                keys = pygame.key.get_pressed()
                self.player.move(keys)
        else:
            if GlobalManager.paused:  # Se o jogo estiver pausado
                self.pause_menu.run()
            elif GlobalManager.on_inventory:  # Se o jogador estiver no inventário
                self.infos_hud.update()
                self.infos_hud.draw()

        # Atualiza a tela
        pygame.display.flip()

    def on_last_execution(self):
        self.__execution_counter = 0
        self.map_loaded = False
    
    @property
    def execution_counter(self):
        return self.__execution_counter

    @property
    def display(self):
        return self.__display
    
    @property
    def name(self):
        return self.__name
    
    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value

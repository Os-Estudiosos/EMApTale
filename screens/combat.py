import pygame
from screens import State

from config import *

from classes.battle.button import CombatButton
from classes.battle.container import BattleContainer
from classes.battle.hp_container import HPContainer
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.battle.menus.main_menu import MainMenu
from classes.battle.menus.inventory_menu import InventoryMenu
from classes.battle.menus.act_menu import ActMenu
from classes.battle.menus.fight_menu import FightMenu
from classes.battle.menus.mercy_menu import MercyMenu

from classes.text.dynamic_text import DynamicText
from classes.text.text import Text

from config.globalmanager import GlobalManager
from config.soundmanager import SoundManager
from config.fontmanager import FontManager
from config.combatmanager import CombatManager
from config.eventmanager import EventManager
from config.gamestatemanager import GameStateManager

from classes.battle.heart import Heart
from classes.player import Player

from constants import *

import time


class Combat(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__variables = {}
        self.__name = name
        self.__display: pygame.Surface = display

        self.__execution_counter = 0

        # Criando os groups de sprites
        self.text_groups = pygame.sprite.Group()  # Grupo dos textos
        self.player_group = pygame.sprite.Group()  # Grupo do player
        CombatManager.set_variable('player_group', self.player_group)

        # Adiciono dois canais específicos
        SoundManager.add_chanel()
        SoundManager.add_chanel()

        # ============ VARIÁVEIS DO HUD ============
        # Carregando o background da batalha
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'battle-background.png')),
            (self.__display.get_width()/1.2, 300)
        )
        self.background_rect = self.background.get_rect()
        self.background_rect.centerx = self.__display.get_width()/2
        self.background_rect.y = 10

        # Iniciando o container da Batalha
        self.battle_container = BattleContainer(self.__display)
        CombatManager.set_variable('battle_container', self.battle_container)

        # Variáveis do Jogador
        self.player = Heart(self.battle_container, self.player_group)
        CombatManager.set_variable('player', self.player)

        # Texto que aparece no inicio da batalha
        self.starter_text = DynamicText(
            '',
            FontManager.fonts['Gamer'],
            22,
            int((450*100)/self.__display.get_height()),
            sound='text_2.wav'
        )

        # Definindo todos os menus
        self.main_menu = MainMenu(self.__display)
        self.inventory_menu = InventoryMenu(self.battle_container)
        self.act_menu = ActMenu(self.battle_container)
        self.fight_menu = FightMenu()
        self.mercy_menu = MercyMenu(self.battle_container)

        BattleMenuManager.menus = {
            f'{self.main_menu.__class__.__name__}': self.main_menu,
            f'{self.inventory_menu.__class__.__name__}': self.inventory_menu,
            f'{self.act_menu.__class__.__name__}': self.act_menu,
            f'{self.fight_menu.__class__.__name__}': self.fight_menu,
            f'{self.mercy_menu.__class__.__name__}': self.mercy_menu,
        }


        # Variáveis de teste para game over
        self.heart_sherd = [
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "player", "hearts", 'broken-heart.png')),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "player", "hearts", 'heart-sherd-1.png')),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "player", "hearts", 'heart-sherd-2.png')),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "player", "hearts", 'heart-sherd-3.png'))
        ]
        self.control_time = 2000


    def on_first_execution(self):
        # Limpando os sons
        self.__execution_counter += 1
        SoundManager.stop_music()
        self.act_menu.options.clear()
        self.act_menu.options = self.__variables['enemy']['act']

        CombatManager.turn = 'player'
        BattleMenuManager.active_menu = 'MainMenu'

        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), 'sounds', CombatManager.enemy.music))

        self.starter_text.restart(self.__variables['enemy']['starter_text'])

        Player.load_infos()

        # Variáveis para quando o Boss morrer
        self.opacity_helper_surface = pygame.Surface(self.__display.get_size(), pygame.SRCALPHA)
        self.opacity_helper_surface.fill(pygame.Color(0,0,0,0))

        self.transition_rate = FPS

        self.transition_counter = 0

        self.white_transition_surface = pygame.Surface(self.__display.get_size(), pygame.SRCALPHA)
        self.transition_alpha = 0
        self.transition_counter = 0
        self.white_transition_surface.fill(pygame.Color(255,255,255,self.transition_alpha))
        self.opacity_helper_surface.blit(self.white_transition_surface, self.white_transition_surface.get_rect())

        self.go_to_next_screen_transition_time = FPS  # Demora 1 segundo para sair do combate e ir pro próximo dia
        self.go_to_next_screen_transition_measurer = 0

    def handle_events(self):
        for event in EventManager.events:
            if event.type == BOSS_TURN_EVENT:
                self.player.apply_effect('normal')
                CombatManager.set_boss_turn()
                CombatManager.enemy.choose_attack()
                CombatManager.enemy.dialogue.restart()
                CombatManager.enemy.speak()
                pygame.time.set_timer(BOSS_TURN_EVENT, 0)
            if event.type == PLAYER_TURN_EVENT:
                BattleMenuManager.change_active_menu('MainMenu')
                CombatManager.set_player_turn()
                pygame.time.set_timer(PLAYER_TURN_EVENT, 0)
            if event.type == BOSS_HITTED:
                damage_taken = self.player.inventory.equiped_weapon.damage*(1-(event.absolute_difference)/(self.battle_container.inner_rect.width/2))
                CombatManager.enemy.take_damage(
                    damage_taken
                )


    def brake_heart_animation(self, heart_position, sprites):
        scale_factor = 1.3  
        broken = sprites[0]
        sherd_1 = pygame.transform.scale_by(sprites[1], scale_factor)
        sherd_2 = pygame.transform.scale_by(sprites[2], scale_factor)
        sherd_3 = pygame.transform.scale_by(sprites[3], scale_factor)
        sherd_4 = pygame.transform.scale_by(sprites[3], scale_factor)
        sherd_5 = pygame.transform.scale_by(sprites[2], scale_factor)
        sherd_6 = pygame.transform.scale_by(sprites[2], scale_factor)

        # Variáveis para manipular o movimento dos cacos
        sherd_positions = [list(heart_position) for n in range(6)]
        sherd_speed = [(-1, -3), (0, -3), (2, -3), (-2, 1), (-1, -5), (-2, -1)]  # Velocidades iniciais (x, y)
        gravity = 0.1

        # Delay
        delay_broken_to_sherds = 2000  
        start_time = pygame.time.get_ticks() 

        stage = "broken"  
        running = True

        while running:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time  

            # Limpar tela
            self.__display.fill((0, 0, 0))

            if stage == "broken":
                broken_rect = broken.get_rect(center=heart_position)
                self.__display.blit(broken, broken_rect)

                if elapsed_time >= delay_broken_to_sherds:
                    SoundManager.play_sound('break_heart_2.wav')
                    stage = "sherds"  

            elif stage == "sherds":
                for i, (vx, vy) in enumerate(sherd_speed):
                    sherd_positions[i][0] += vx  # Atualizar posição x
                    sherd_positions[i][1] += vy  # Atualizar posição y
                    sherd_speed[i] = (vx, vy + gravity)  

                # Desenhar os cacos
                self.__display.blit(sherd_1, sherd_positions[0])
                self.__display.blit(sherd_2, sherd_positions[1])
                self.__display.blit(sherd_3, sherd_positions[2])
                self.__display.blit(sherd_4, sherd_positions[3])
                self.__display.blit(sherd_5, sherd_positions[4])
                self.__display.blit(sherd_6, sherd_positions[5])

            pygame.display.flip()

            clock = pygame.time.Clock()
            clock.tick(60)

            if elapsed_time > 4500:
                GameStateManager.set_state('gameover_cutscene')
                return


    def run(self):
        # Inicio do ciclo de vida da cena
        if not self.__execution_counter > 0:
            self.on_first_execution()
        
        # ============ GAME OVER ============
        if Player.life == 0:
            # Parar todas as ações, deixar fundo preto
            pygame.time.set_timer(BOSS_TURN_EVENT, 0)
            pygame.time.set_timer(PLAYER_TURN_EVENT, 0)
            self.__display.fill((0, 0, 0))
            SoundManager.stop_music()

            # Obter a posição do coração
            heart_position = self.player.rect.center
    
            # Desenhar o coração na última posição
            self.player_group.draw(self.__display)
            SoundManager.play_sound('break_heart_1.wav')
            self.brake_heart_animation(heart_position, self.heart_sherd)    
            return


        self.handle_events()
        
        # Ajustando o nome do personagem
        text_player_name = Text(self.player.name.upper(), FontManager.fonts['Gamer'], 60)
        text_player_name.rect.x = self.main_menu.options[0].rect.x
        text_player_name.rect.y = self.main_menu.options[0].rect.y - 1.5*text_player_name.rect.height

        # Ajustando o HP do personagem (Na tela)
        hp_container = HPContainer()
        hp_container.inner_rect.center = [
            self.__display.get_width()/2,
            text_player_name.rect.centery
        ]

        # ============ DESENHANDO O BACKGROUND ============
        self.__display.blit(self.background, self.background_rect)

        # ============ DANDO UPDATE NOS ELEMENTOS GERAIS ============
        self.battle_container.update()
        hp_container.update()
        self.battle_container.update()
        self.main_menu.update()
        CombatManager.enemy.update()

        # ============ DESENHANDO TUDO ============
        CombatManager.enemy.draw(self.__display)
        self.battle_container.draw()
        text_player_name.draw(self.__display)
        hp_container.draw(self.__display)
        self.main_menu.draw()
        CombatManager.draw_global_groups(self.__display)

        # Ajustando o container da batalha para ficar em cima da vida do jogador
        self.battle_container.out_rect.bottom = hp_container.inner_rect.bottom - 50

        # Pegando as teclas apertadas
        keys = pygame.key.get_pressed()

        # ============ CÓDIGO RELACIONADO AOS TURNOS ============
        # Se for o turno do Player
        if CombatManager.turn == 'player':
            # ============ HUD QUE SÓ APARECE NO TURNO DO PLAYER ============
            # Esse monte de self.option é para deixar numa largura onde o lado esquerdo fica alinhado com o primeiro botão e o direito com o útlimo botão
            self.battle_container.resize(
                self.main_menu.options[len(self.main_menu.options)-1].rect.right - self.main_menu.options[0].rect.left,
                abs(CombatManager.enemy.rect.bottom - self.battle_container.out_rect.bottom)
            )  # Redesenho o container da batalha

            # Ajustando os botões do HUD
            for i, button in enumerate(self.main_menu.options):
                if i == self.main_menu.selected_option:  # Se o botão que eu estiver analisando for a opção selecionada
                    button.activated = True  # Eu marco a propriedade de ativado
                else:
                    button.activated = False  # Eu removo a propriedade de ativado
                    
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                # Só permito mexer de novo o cursor se eu soltar a tecla e apertar de novo
                self.trying_to_move_cursor = False

            # ========== ATUALIZANDO E DESENHANDO AS COISAS QUE SÓ APARECEM NO TURNO DO PLAYER ==========
            if BattleMenuManager.active_menu != 'MainMenu':
                BattleMenuManager.update()
                BattleMenuManager.draw()
            else:
                self.starter_text.max_length = self.battle_container.inner_rect.width-20
                self.starter_text.position = (
                    self.battle_container.inner_rect.x + 10,
                    self.battle_container.inner_rect.y + 10,
                )
                self.starter_text.update()
                self.starter_text.draw(self.__display)

        elif CombatManager.turn == 'boss':  # Se não for o turno do player
            for btn in self.main_menu.options:  # Ajustando para nenhum botão ficar selecionado
                btn.activated = False
        
            if not CombatManager.enemy.dead:
                self.battle_container.resize(self.__display.get_width()/3, self.__display.get_height()/2-30)  # Redimensiono o container da batalha
                
                # Updates que são apenas do turno do boss
                self.player.update(display=self.__display)

                # Draws que são apenas no turno do boss
                self.player.draw(self.__display)
        
        if CombatManager.enemy.dead:
            if self.transition_counter == 0:
                SoundManager.stop_music()
                SoundManager.play_sound('cymbal.ogg', 1)
                self.go_to_next_screen_transition_measurer = pygame.time.get_ticks()
            
            self.transition_counter += 1
            
            if self.transition_counter%self.transition_rate == 0 and self.transition_alpha + 1 <= 255:
                self.transition_alpha += 1

            self.white_transition_surface.fill(pygame.Color(255,255,255,self.transition_alpha))

            self.opacity_helper_surface.blit(self.white_transition_surface, self.white_transition_surface.get_rect())    

            self.__display.blit(self.opacity_helper_surface, self.opacity_helper_surface.get_rect())

            if not SoundManager.is_chanel_playing(1):
                actual_ticks = pygame.time.get_ticks()
                if actual_ticks - self.go_to_next_screen_transition_measurer >= 2000:
                    GameStateManager.set_state('show_day')
        
        CombatManager.execute_global_draws(display=self.__display)

    def on_last_execution(self):
        self.__execution_counter = 0
        CombatManager.enemy.restart_attacks()

    @property
    def execution_counter(self):
        return self.execution_counter

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

        CombatManager.set_boss(self.__variables['enemy'])

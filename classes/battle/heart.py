import pygame
import os
from config import GET_PROJECT_PATH
from utils import sign
from classes.battle.container import BattleContainer


class Heart(pygame.sprite.Sprite):
    def __init__(self, container: BattleContainer, *groups):
        """Inicialização da classe

        Args:
            container (BattleContainer): O Container da batalha, servirá para detecção da colisão
        """
        super().__init__(*groups)

        self.sprites: dict[str, pygame.Surface] = {
            'normal': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
                1.3
            ),
            'laugh': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'branco-heart.png')),
                1.3
            ),
            'inverse': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'yuri-heart.png')),
                1.3
            ),
            'confused': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'walter-heart.png')),
                1.3
            ),
            'prisioned': pygame.transform.scale_by(
                pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'soledad-heart.png')),
                1.3
            )
        }

        self.image = self.sprites['normal']
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (
            pygame.display.get_window_size()[0]/2,
            pygame.display.get_window_size()[1]/2
        )
        
        self.container: BattleContainer = container

        self.effect = 'normal'

        self.speed = 3
    
    def apply_effect(self, effect: str):
        self.image = self.sprites[effect]
        self.effect = effect
    
    def update(self, *args, **kwargs):
        keys = pygame.key.get_pressed()

        # # Movimentação
        direction = pygame.math.Vector2(  # Faço um vetor que representa a direção que estou me movendo
            sign(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]),
            sign(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        )

        if direction.length() != 0:  # Normalizo para andar sempre na mesma velocidade
            direction = direction.normalize()

        if self.effect == 'inverse':  # Aplico efeito da inversa se tiver
            direction = pygame.math.Vector2(
                direction.x * -1,
                direction.y * -1
            )

        # Mexendo na colisão
        # Esse código detecta se um ponto na frente do player está saindo do retangulo, se sair, eu paro de mexer o player
        if not self.container.out_rect.collidepoint(self.rect.centerx + (self.speed+self.mask.get_rect().width/2-7)*direction.x, self.rect.centery):
            direction.x = 0
        if not self.container.out_rect.collidepoint(self.rect.centerx, self.rect.centery + (self.speed+self.mask.get_rect().height/2-7)*direction.y):
            direction.y = 0

        # Mexo na posição
        self.rect.x += self.speed * direction.x
        self.rect.y += self.speed * direction.y

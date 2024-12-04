import pygame
import os

FPS = 60  # FPS Máximo
GAME_NAME = 'EMApTale'  # Nome da Janela

MAP_SCALE_FACTOR = 2.5

def GET_PROJECT_PATH():  # Retorna a pasta do projeto independente do Sistema Operacional
    return os.getcwd()

import pygame


class BattleMenuManager:
    active_menu = 'MainMenu'

    @classmethod
    def change_active_menu(cls, menu_name: str):
        cls.active_menu = menu_name

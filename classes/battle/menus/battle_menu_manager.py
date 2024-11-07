import pygame

class BattleMenuManager:
    active_menu = None
    menus = {}

    @classmethod
    def change_active_menu(cls, menu_name: str):
        if menu_name in cls.menus.keys():
            cls.active_menu = cls.menus[menu_name]
        elif menu_name == 'MainMenu':
            cls.active_menu = None

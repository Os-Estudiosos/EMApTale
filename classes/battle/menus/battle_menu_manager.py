import pygame

class BattleMenuManager:
    active_menu = 'MainMenu'
    previous_menu = None
    menus = {}

    @classmethod
    def change_active_menu(cls, menu_name: str):
        if menu_name in cls.menus.keys():
            cls.previous_menu = cls.active_menu
            cls.active_menu = cls.menus[menu_name]
    
    @classmethod
    def go_back(cls):
        cls.active_menu = cls.previous_menu

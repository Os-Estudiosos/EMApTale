import unittest
import sys
import os
from uuid import uuid4
sys.path.append(os.getcwd())
from classes.inventory import Inventory
from classes.item import Item


class InventoryTests(unittest.TestCase):
    def test_adding_item(self):
        """Testando se está adicionando itens corretamente"""
        inv = Inventory()

        test_item = Item({
            "name": "Pão de Queijo",
            "type": "miscellaneous",
            "description": "O pão de queijo mais cobiçado do prédio",
            "effect": "heal",
            "after_effect_text": "A fama desse negócio na EMAp tem motivo! Você curou 10 de vida",
            "value": 10
        })

        inv.add_item(test_item)

        self.assertEqual(inv, [test_item])
    
    def test_adding_item_errors(self):
        """Testando se adicionar itens está levantando os erros corretamente"""
        inv = Inventory()

        self.assertRaises(TypeError, inv.add_item, 1)
        self.assertRaises(TypeError, inv.add_item, '1')
        self.assertRaises(TypeError, inv.add_item, ())
        self.assertRaises(TypeError, inv.add_item, [])
        self.assertRaises(TypeError, inv.add_item, complex(1, 2))

        self.assertRaises(KeyError, inv.add_item, {})


    def test_removing_item(self):
        """Testando se está removendo itens corretamente"""
        inv = Inventory()

        test_item = Item({
            "name": "Pão de Queijo",
            "type": "miscellaneous",
            "description": "O pão de queijo mais cobiçado do prédio",
            "effect": "heal",
            "after_effect_text": "A fama desse negócio na EMAp tem motivo! Você curou 10 de vida",
            "value": 10
        })

        item_id = inv.add_item(test_item)

        inv.remove_item(item_id)

        self.assertEqual(inv.items, [])
    
    def test_removing_item_errors(self):
        """Testando se o método de remover itens está levantando os erros corretamente"""
        inv = Inventory()

        self.assertRaises(TypeError, inv.remove_item, 1)
        self.assertRaises(TypeError, inv.remove_item, '1')
        self.assertRaises(TypeError, inv.remove_item, {})
        self.assertRaises(TypeError, inv.remove_item, ())
        self.assertRaises(TypeError, inv.remove_item, complex(1,1))
        self.assertRaises(TypeError, inv.remove_item, [])
    
    def test_getting_item(self):
        """Testando se está retornando os itens corretamente"""
        inv = Inventory()

        test_item = Item({
            "name": "Pão de Queijo",
            "type": "miscellaneous",
            "description": "O pão de queijo mais cobiçado do prédio",
            "effect": "heal",
            "after_effect_text": "A fama desse negócio na EMAp tem motivo! Você curou 10 de vida",
            "value": 10
        })

        item_id = inv.add_item(test_item)

        self.assertEqual(inv.get_item(item_id), test_item)
    
    def test_getting_item_errors(self):
        """Testando se o método de pegar itens está levantando corretamente os erros"""

        inv = Inventory()

        self.assertRaises(TypeError, inv.remove_item, 1)
        self.assertRaises(TypeError, inv.remove_item, '1')
        self.assertRaises(TypeError, inv.remove_item, {})
        self.assertRaises(TypeError, inv.remove_item, ())
        self.assertRaises(TypeError, inv.remove_item, complex(1,1))
        self.assertRaises(TypeError, inv.remove_item, [])

        self.assertRaises(ValueError, inv.remove_item, uuid4())
    
    def test_equiping_weapon(self):
        ...

    def test_equiping_weapong_errors(self):
        ...

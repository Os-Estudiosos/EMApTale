import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd()))

from classes.inventory import Inventory, Item

class InventoryTests(unittest.TestCase):
    def test_adding_dict_items(self):
        """Testando o método de adicionar itens no inventário como dicionários
        """
        # Adicionando por dicionários
        items = [
            {
                "name": "banana",
                "type": "miscellaneous",
                "description": "Uma banana"
            },
            {
                "name": "faca",
                "type": "weapon",
                "description": "Uma arma bem afiada"
            }
        ]
        inventory = Inventory()
        
        for item in items:
            inventory.add_item(item)
        
        for i, itm in enumerate(inventory):
            self.assertEqual(vars(itm), items[i])
    
    def test_adding_item_items(self):
        items = [
            Item({
                "name": "banana",
                "type": "miscellaneous",
                "description": "Uma banana"
            }),
            Item({
                "name": "faca",
                "type": "weapon",
                "description": "Uma arma bem afiada"
            })
        ]
        inventory = Inventory()

        for item in items:
            inventory.add_item(item)
        
        self.assertEqual(inventory.items, items)
    
    def test_adding_wrong_items(self):
        """Testando se está levantando erro ao passar o tipo errado pro inventário
        """
        inventory = Inventory()
        with self.assertRaises(TypeError):
            inventory.add_item(1)
            inventory.add_item('24')
            inventory.add_item([])
            inventory.add_item({1, 2, 3})
    
    def test_removing_items(self):
        """Testando o método de remover os itens
        """
        # Adicionando por dicionários
        items = [
            {
                "name": "banana",
                "type": "miscellaneous",
                "description": "Uma banana"
            },
            {
                "name": "faca",
                "type": "weapon",
                "description": "Uma arma bem afiada"
            }
        ]
        inventory = Inventory()
        
        for item in items:
            inventory.add_item(item)
        
        inventory.remove_item(0)
        items.pop(0)
        
        for i, itm in enumerate(inventory):
            self.assertEqual(vars(itm), items[i])
    
    def test_removing_wrong_items(self):
        """Teste se levanta erro ao passar parâmetros errados para o método de remover itens
        """
        # Adicionando por dicionários
        items = [
            {
                "name": "banana",
                "type": "miscellaneous",
                "description": "Uma banana"
            },
            {
                "name": "faca",
                "type": "weapon",
                "description": "Uma arma bem afiada"
            }
        ]
        inventory = Inventory()
        
        with self.assertRaises(TypeError):
            inventory.remove_item(1.3)
            inventory.remove_item('a')
            inventory.remove_item({})
            inventory.remove_item([1.2])
            inventory.remove_item({1,2,3})
        
        with self.assertRaises(ValueError):
            inventory.remove_item(5)
            inventory.remove_item(-27)

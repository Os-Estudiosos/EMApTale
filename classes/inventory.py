class Inventory:
    def __init__(self, items: list = []):
        self.items = []
        for item in items:
            self.add_item(item)
        self.equpied_weapon = None

    
    def add_item(self, item):
        """Método que adiciona um item no inventário

        Args:
            item (dict|Item): Dicionário com as informações do item ou uma instância de um item
        """
        from classes.item import Item

        if isinstance(item, dict):
            self.items.append(Item(item))
        elif isinstance(item, Item):
            self.items.append(item)
        else:
            raise TypeError("Você precisa passar um dicionário ou uma instância de Item")
    
    def remove_item(self, id: int):
        """Método que remove um item do inventário

        Args:
            id (int): ID do item que vai ser removido
        """
        if not isinstance(id, int):
            raise TypeError("Passe um número inteiro como parâmetro")
        if id < 0 or id >= len(self.items):
            raise ValueError("O id passado não é válido")
        self.items.pop(id)

    def equip_weapon(self, id: int):
        """Equipa a arma com o ID passado

        Args:
            id (int): ID da arma que vai ser equipado
        """
        if not isinstance(id, int):
            raise TypeError("Passe um número inteiro como parâmetro")
        if id < 0 or id >= len(self.items):
            raise ValueError("O id passado não é válido")
        
        if self.items[id].type == 'weapon':
            self.equpied_weapon = self.items[id] 

    def __eq__(self, value: list):
        return self.items == value

    def __iter__(self):
        return iter(self.items)

    def __next__(self):
        return next(iter(self.items))

class Inventory:
    def __init__(self, items: list = []):
        self.items = []
        self.equiped_weapon = []
        for item in items:
            self.add_item(item)
            if item['equiped']:
                self.equip_weapon(item['id'])

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
    
    def remove_item(self, id: str):
        """Método que remove um item do inventário

        Args:
            id (str): ID do item que vai ser removido
        """
        if not isinstance(id, str):
            raise TypeError("Passe um número inteiro como parâmetro")
        return list(filter(lambda item: item.id != id, self.items))
     
    def get_item(self, id: str):
        """Pega um item pelo ID

        Args:
            id (str): ID do item
        """
        for item in self.items:
            if item.id == id:
                return item
        else:
            raise ValueError('O Id passado não está no inventário')

    def equip_weapon(self, id: str):
        """Equipa a arma com o ID passado

        Args:
            id (str): ID da arma que vai ser equipado
        """
        if not isinstance(id, str):
            raise TypeError("Passe um número inteiro como parâmetro")
        
        self.equiped_weapon = self.get_item(id)

    def __eq__(self, value: list):
        return self.items == value

    def __iter__(self):
        return iter(self.items)

    def __next__(self):
        return next(iter(self.items))

from uuid import uuid4, UUID


class Inventory:
    def __init__(self, items: list = []):
        self.items = []
        self.equiped_weapon = None
        for item in items:
            self.add_item(item)
            if item['type'] == 'weapon' and item['equiped']:
                self.equip_weapon(item['id'])

    def add_item(self, item):
        """Método que adiciona um item no inventário

        Args:
            item (dict|Item): Dicionário com as informações do item ou uma instância de um item
        """
        from classes.item import Item

        if isinstance(item, dict):
            new_item_uuid = uuid4()
            item['id'] = new_item_uuid
            self.items.append(Item(item))
            return new_item_uuid
        elif isinstance(item, Item):
            self.items.append(item)
            return item.id
        else:
            raise TypeError("Você precisa passar um dicionário ou uma instância de Item")
    
    def remove_item(self, id: UUID):
        """Método que remove um item do inventário

        Args:
            id (str): ID do item que vai ser removido
        """
        if not isinstance(id, UUID):
            raise TypeError("Passe um UUID como parâmetro")

        self.items = list(filter(lambda item: item.id != id, self.items))
     
    def get_item(self, id: UUID):
        """Pega um item pelo ID

        Args:
            id (str): ID do item
        """
        if not isinstance(id, UUID):
            raise TypeError("Passe um UUID como ")

        if len(self.items) == 0:
            raise ValueError('O Inventário está vazio')

        for item in self.items:
            if item.id == id:
                return item
        else:
            raise ValueError('O Id passado não está no inventário')

    def equip_weapon(self, id: UUID):
        """Equipa a arma com o ID passado

        Args:
            id (str): ID da arma que vai ser equipado
        """
        if not isinstance(id, UUID):
            raise TypeError("Passe um UUID parâmetro")
        
        self.equiped_weapon = self.get_item(id)

    def __len__(self):
        return len(self.items)

    def __eq__(self, value: list):
        return self.items == value

    def __iter__(self):
        return iter(self.items)

    def __next__(self):
        return next(iter(self.items))

    def __getitem__(self, index):
        return self.items[index]
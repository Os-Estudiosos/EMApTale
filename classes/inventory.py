
class Item:
    def __init__(self, properties):
        self.__dict__ = properties


class Inventory:
    def __init__(self, items: list):
        self.items = []
        for item in items:
            self.items.append(Item(item))
    
    def __iter__(self):
        return iter(self.items)

    def __next__(self):
        return next(iter(self.items))

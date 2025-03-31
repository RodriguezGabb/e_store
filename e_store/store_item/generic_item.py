from abc import ABC, abstractmethod
"""classe astratta per gli item con un prezzo"""
class GenericItem(ABC):
    def __init__(self, name:str, price:float)->None:
        self.name = name
        self.price = price
        #foreign è un campo booleano che viene impostato durante la creazione del oggetto
        self.foriegn=False #default value

    def get_price(self)->float:
        """ritorna il prezzo dell'item"""
        if self.foriegn:
            return self.price*1.2
        else:
            return self.price
    
    def __str__(self):
        return f"nome: {self.name} price: {self.price} foreign: {self.foriegn}"
    
#Normal Item
class NormalItem(GenericItem):
    foriegn=False
    
#Foreign Item
class ForeignItem(GenericItem):
    foriegn=True
    
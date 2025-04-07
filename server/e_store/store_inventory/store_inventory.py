from typing import Any, Dict
from e_store.store_item.generic_item import GenericItem as Item


class StoreInventory:
    """Classe che gestisce l'inventario del negozio"""
    def __init__(self)->None:
        #Un dizzionario che ha per chiave i nomi dei oggetti e per valore un dizionario con chiave l'oggetto stesso e come valore la quantità
        self.inventory:Dict[str, Dict[str, Any]] = {}

    def add_product(self, product:Item, product_quantity):
        """Aggiunge un prodotto all'inventario"""
        self.inventory[product.name] = {'product':product,'quantity':product_quantity}

    def remove_product(self, product_name:str, quantity:int)->bool:
        """Rimuove una certa quantità di prodotto dall'inventario"""
        if product_name in self.inventory and self.inventory[product_name]['quantity'] >= quantity:
            self.inventory[product_name]['quantity'] -= quantity
            return True
        return False

    def get_all_products(self) -> Dict[str, Dict[str, Any]]:
        """Ritorna l'inventario attuale"""
        return self.inventory
    
    def __str__(self):
        return f"inventory: {self.inventory}"
    
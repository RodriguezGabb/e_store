from e_store.store_inventory.store_inventory import StoreInventory
from e_store.customer.generic_customer import GenericCustomer as Customer

class Store:
    """Classe che contiene l'inventario e il saldo del negozzio"""
    def __init__(self, money:float) -> None:
        self.inventory = StoreInventory()
        self.money = money

    def sell_item(self, customer:Customer, product_name:str,quantity:int)->bool:
        """Vende un prodotto a un cliente se possibile"""
        if product_name in self.inventory.get_all_products():
             product_info=self.inventory.get_all_products()[product_name]
             final_price=product_info['product'].get_price()*quantity
             if self.inventory.remove_product(product_name,quantity) and customer.buy(final_price):
                 self.money+=final_price
                 return True
        return False
            
                     

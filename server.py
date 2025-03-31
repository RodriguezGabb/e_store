from typing import Dict, List
from pydantic import BaseModel
from fastapi import FastAPI
from e_store.customer.generic_customer import *
from e_store.store.store import Store
from e_store.store_item.generic_item import GenericItem, NormalItem, ForeignItem
'''GET: get_inventory: che lista tutti gli oggetti nell’inventario con le loro quantità e il loro
prezzo'''

app=FastAPI(title="e-store API")

#creazione del magazino
magazzino = Store(1000)
#crazione dei vari prodotti
Apple=NormalItem("Apple", 1)
Banana=ForeignItem("Banana", 10)
Orange=ForeignItem("Orange", 100)
Pear=NormalItem("Pear", 5)
#aggiunta al magazzino
magazzino.inventory.add_product(Apple, 10)
magazzino.inventory.add_product(Banana, 50)
magazzino.inventory.add_product(Orange, 100)
magazzino.inventory.add_product(Pear, 25)
#creazione dei clienti
Martina= PromotionalCustomer("Martina", "Pennella", 1000, "1234")
Gabriel= NormalCustomer("Gabriel", "Rodriguez", 1000, "4321")

#creazione del dizionario con i clienti
customers_dic: Dict[str, GenericCustomer] = {"Martina": Martina, "Gabriel": Gabriel}


class InventoryItem(BaseModel):
    name: str
    quantity: int
    price: float
    
class UserItem(BaseModel):
    name:str
    quantity:int
    


@app.get("/inventory",response_model=InventoryItem)
def get_inventory()-> List[InventoryItem]:
    res: List[InventoryItem]=[]
    for name, info in magazzino.inventory.get_all_products().product():
        res.append(
            InventoryItem(
                name=name,
                quantity=info["quantity"],
                price=info["item"].get_price()
            )
        )
    return res

@app.get("/user/{username}/items",response_model=UserItem)
def get_user_items(username)-> List[UserItem]:
    #controllo se l'user esiste
    if (username not in customers_dic):
        raise Exception("Utente {username} non trovato!")
    user=customers_dic[username]
    res: List[UserItem]=[]
    for item_name, item_quantity in user.inventory.items():
        res.append(
            UserItem(
                name= item_name,
                quantity= item_quantity
            )
        )
    return res

'''Avvio del server'''   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    

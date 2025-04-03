from typing import Dict, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from customer.generic_customer import *
from store.store import Store
from store_item.generic_item import GenericItem, NormalItem, ForeignItem
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

class ItemInformation(BaseModel):
    name:str
    price:float
    quantity:int

class UserBalance(BaseModel):
    username: str
    balance: float

class PurchaseRequest(BaseModel):
    username:str
    pswd:str
    item_name:str
    quantity:int

class PurchaseValidation(BaseModel):
    validation:bool
    message:str

@app.get("/")
def read_root():
    return {"message": "Hello from the e_store server"}
@app.get("/inventory")
def get_inventory()-> List[InventoryItem]:
    res: List[InventoryItem]=[]
    for name, info in magazzino.inventory.get_all_products().items():
        res.append(
            InventoryItem(
                name=name,
                quantity=info["quantity"],
                price=info["product"].get_price()
            )
        )
    return res

@app.get("/user/{username}/items")
def get_user_items(username:str)-> List[UserItem]:
    #controllo se l'user esiste
    if (username not in customers_dic):
        raise HTTPException(status_code=404, detail=f"User {username} not found!")
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

@app.get("/item/{item_name}")
def get_item_information(item_name:str)->ItemInformation:
    inventory= magazzino.inventory.get_all_products()
    if item_name not in inventory:
        raise HTTPException(status_code=404, detail=f"Item {item_name} not found ")
    res= ItemInformation(
        name=item_name,
        price=inventory[item_name]["product"].get_price(),
        quantity=inventory[item_name]["quantity"]
    )
    return res

@app.get("/user/{username}/balance")
def get_balance(username:str)->UserBalance:
    if (username not in customers_dic):
        raise HTTPException(status_code=404, detail=f"User {username} not found!")
    user=customers_dic[username]
    res=UserBalance(
        username=username,
        balance=user.money
    ) 
    return res

@app.post("/purchase")
def purchase(request:PurchaseRequest)->PurchaseValidation:
    quantity=request.quantity
    #controllo user
    if request.username not in customers_dic:
        return PurchaseValidation(
            validation=False,
            message=f"User {request.username} not found!"
        )

    user=customers_dic[request.username]
    #controllo password
    if request.pswd != user.password:
        return PurchaseValidation(
            validation=False,
            message=f"The password is incorect!"
        )
        
    inventory= magazzino.inventory.get_all_products()
    #controllo item
    if request.item_name not in inventory:
        return PurchaseValidation(
            validation=False,
            message=f"Item {request.item_name} not found "
        )
    
    item=inventory[request.item_name]
    #controllo la quantità
    if quantity> item["quantity"]:
        return PurchaseValidation(
            validation=False,
            message=f"The quantity requested of {request.item_name} is higher than the quantity in the inventoory"
        )
    
    item_price: float=item["product"].get_price()
    total_cost: float= item_price * quantity
    if user.money<total_cost:
        return PurchaseValidation(
            validation=False,
            message=f"The total price is {total_cost} but you only have {user.money} on your acount"
        )
    
    if magazzino.sell_item(user,request.item_name,request.quantity):
        user.add_item(request.item_name,quantity)
        return PurchaseValidation(
            validation=True,
            message=f"purchase of {quantity} {request.item_name} successful"
        )
        
    else:
        return PurchaseValidation(
            validation=False,
            message=f"Purchase faild, a error occured"
        )
        

'''Avvio del server se lo avvio da server.py'''   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    

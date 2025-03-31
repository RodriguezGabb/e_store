from typing import Any, Dict
from customer.generic_customer import NormalCustomer, PromotionalCustomer, GenericCustomer
from store.store import Store
from store_item.generic_item import NormalItem, ForeignItem

def login(customers:Dict)->GenericCustomer:
    """Take a dictionary of customers and make the user login.
        or return -1 in case of error"""
    username = input("Enter username: ")
    while not username in customers:
        if username.lower()=="quit":
            return -1
        print("User not found!\n Try again or type 'quit' to exit")
        username = input("Enter username: ")
        
    pws= input("Enter password: ")
    while customers[username].password!=pws:
        if pws.lower()=="quit":
            return -1
        print("Wrong password!\n Try again or type 'quit' to exit")
        pws= input("Enter password: ")
        
    print("Login successful!")
    return customers[username]


def run_store()->None:
    """Run the store simulation."""
    running=True
    #creazione del magazzino
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
    customer=login(customers_dic)
    if customer==-1:
        print("quitting...")
        running=False


    while running:

        print(f"Your money: {customer.money}")
        print("Store Inventory:")
        for name, info in magazzino.inventory.get_all_products().items():
            print(f"{name}: {info['quantity']} available at {info['product'].get_price()} each")
        
        choice = input("Enter item to buy or 'quit' to exit: ")
        if choice == "quit":
            print("quitting...")
            break
        
        quantity = int(input("Enter quantity: "))
        
        if magazzino.sell_item(customer, choice, quantity):
            print("Purchase successful!")
        else:
            print("Purchase failed!")
        
        print()

from abc import ABC, abstractmethod
from typing import Dict

"""Discounts of the customers"""
DISCOUNTNORMAL = 1
DISCOUNTPROMOTIONAL = 0.95
"""Abstract class for the customers"""
class GenericCustomer(ABC):
    def __init__(self, name:str, surname:str, money:float, password:str)->None:
        self.name = name
        self.surname = surname
        self.money = money
        self.password = password #campo prottetto o campo privato?
        self.discount=1 #default discount
        self.inventory: Dict[str,int]={} #dizzionario con nome oggetto e quantità

    def buy(self, price:float)->bool:
        if self.money>price:
            self.money-=price
            return True
        return False

    def add_item(self,name:str, quantity:int)->None:
        if name not in self.inventory :
            self.inventory[name] = quantity
        else:
            self.inventory[name]+=quantity

    def __str__(self):
        return f"name: {self.name}, surname: {self.surname}, money: {self.money}, discount: {self.discount}, inventory: {self.inventory}"
#Normal Customer
class NormalCustomer(GenericCustomer):
    discount=DISCOUNTNORMAL
#Promotional Customer
class PromotionalCustomer (GenericCustomer):
    discount=DISCOUNTPROMOTIONAL



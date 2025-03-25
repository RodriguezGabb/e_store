from abc import ABC, abstractmethod 
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

    def buy(self, price:float)->bool:
        if self.money>price:
            self.money-=price
            return True
        return False

    def __str__(self):
        return f"{self.name} {self.surname} {self.money} {self.discount}"
#Normal Customer
class NormalCustomer(GenericCustomer):
    discount=DISCOUNTNORMAL
#Promotional Customer
class PromotionalCustomer (GenericCustomer):
    discount=DISCOUNTPROMOTIONAL



import random

class Coupon:
    def __init__(self, date1, date2, discount, category):
        self.date1 = date1
        self.date2 = date2
        self.discount = discount
        self.category = category
        self.code = random.randint(1000000000, 9999999999)
    
    def __repr__(self) -> str:
        return f"{self.date1} -- {self.date2} - {self.code} - {self.category}"
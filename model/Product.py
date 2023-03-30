import uuid
import random

class Product():
    def __init__(self, name, expiry, category, quantity, price):
        self.product_id = str(uuid.uuid4())
        self.serial_number = str(random.randint(100000, 999999))
        self.name = name
        self.expiry = expiry
        self.category = category
        self.quantity = quantity
        self.removeReason = None
        self.price = price
    
    def updateStock(self, quantity):
        if isinstance(quantity, int) and quantity >= 0:  # We need to make sure that the input is valid, the quantities can only be integers equal or greater than 0
            self.quantity = quantity
            return True
        else:
            return False


    def __repr__(self):
        return f"{self.product_id} - {self.name} - {self.category} - {self.quantity}"


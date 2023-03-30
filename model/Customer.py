import uuid
import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies
from model.Product import Product
from util.json_utils import transformToDate

class Customer:
    def __init__(self, name, email, address, dob):
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.email = email
        self.bonus_points = 0
        self.status = "unverified"
        self.verification_token = str(uuid.uuid4())[:5]
        self.dob = dob
        self.tempPass = None
        self.newPass = None
        self.history = []
        self.orders = []   # Stores objects from Order class
        self.shoppingCart = {}
        self.currentTotalShoppingCart = 0

    def verify(self, token):
        if self.verification_token == token:
            self.status = "verified"
            self.verification_token = None
        return self.status == "verified"
    
    def addToHistory(self, productName):
            self.history.append(productName)
    
    def generateTempPass(self):
        self.tempPass = str(uuid.uuid4())[:5]
        return True
    
    def resetPass(self, temp_pass, new_pass):
        if temp_pass == self.tempPass:        # We first make sure that the given temporary password is the same as the one we have defined in our specific product       
            self.newPass = new_pass
            self.tempPass = None
            return True
        else:
            return False      
    
    def editCustomer(self, name, address, dob, status, bonus_points):
        if transformToDate(dob) and (isinstance(bonus_points, int) and bonus_points >= 0):
            self.name = name
            self.address = address
            self.dob = dob
            self.status = status
            self.bonus_points = bonus_points
            return True
        else:
            return False


    def registerOrder(self, order, total):
        self.orders.append(order)
        self.addBonusPoints(int(total))   # Once the order is registered, we also add the Bonus Points according to the amount spent.
        self.shoppingCart.clear()
        self.currentTotalShoppingCart = 0

    def addBonusPoints(self, extra):
        if not ((isinstance(extra, int) and extra > 0)):     # We need to make sure that the input is valid, that it is trying to add integers greater than o
            return False
        else:
            self.bonus_points += extra
            return True
        
    def deleteBonusPoints(self, used):
        self.bonus_points -= used
    
    def __str__(self):
        return f"{self.customer_id} - {self.name} - {self.email} - {self.verification_token}"

    def __repr__(self):
        return f"{self.customer_id} - {self.name} - {self.email} - {self.status}"


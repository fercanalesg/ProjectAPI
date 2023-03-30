import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies

from util.json_utils import JSONEncoder, MyEncoder, transformToDate, generateRandomDate, verifyCard
from model.Order import Order
import datetime
import requests
from random import choice

import copy

class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []
        self.orders = []
        self.categories = []

    def addProduct(self, p):
        self.products.append(p)
    
    def deleteProduct(self, p):
        self.products.remove(p)
    
    def removeProduct(self, p, reason):
        p.quantity = 0
        p.removeReason = reason
    
    def addOrderToShop(self, order):
        self.orders.append(order)

    def reorderList(self):
        tempDict = {}
        needToReorder = []
        for o in self.orders:
            if transformToDate(o.placedDate) < datetime.date.today() and transformToDate(o.placedDate) >= datetime.date.today() - datetime.timedelta(days=7):  # We are interested on the orders that were placed this week
                for prod, q in o.purchasedItems.items(): # If the order was placed this week, we get the items that were purchased and the quantity, and we save them in our temporal dictionary
                    if prod in tempDict:
                        tempDict[prod] += q
                    else:
                        tempDict[prod] = q
        
        for p in self.products:                                      # We iterate through the list of products in our shop
            if p.product_id in tempDict:                              
                if p.quantity < tempDict[p.product_id]:              # For each of the items that were bought on the last week, if the current stock of the item is lower than the quantity that was sold through the week, we need to order more
                    needToReorder.append(p.name)                     # We save the items that we need to reorder in the 'needToReorder' list
        if len(needToReorder) == 0:
            return False
        else:
            return(needToReorder)

    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:                           # We evaluate that any customer with the given address, already exists
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, c):
        self.customers.remove(c)

    def getCustomer(self, cust_id):
        for c in self.customers:
            if c.customer_id == cust_id:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c
    
    def getProduct(self, prod_id):
        for p in self.products:
            if p.product_id == prod_id:
                return p
    
    def setCurrentTotalShoppingCart(self, c):                                       # Function to update the currently total amount in the shopping Cart
        total = 0
        for prod, q in c.shoppingCart.items():                                      # We iterate through the shoppingCart(dictionary) items
            price = self.getProduct(prod).price                                     # We get the price from the product
            total += price*q
        c.currentTotalShoppingCart = total

    def addToShoppingCart(self, cus_id, product, addQuantity): 
        c = self.getCustomer(cus_id)
        if not((isinstance(addQuantity, int) and addQuantity > 0) or addQuantity == -1):                # We check that the given quantity is valid, either an integer or -1
            return "Not Valid"
        else:
            if addQuantity == -1:                                           # If the quantity is set to -1 we delete the item from the shopping cart
                if product.product_id in c.shoppingCart:                      # We will do the action only if the product exists in the shopping cart
                    del c.shoppingCart[product.product_id]
                    self.setCurrentTotalShoppingCart(c)
                    return True
                else:
                    return False
            else:
                if product.quantity >= addQuantity:                          # We need to make sure that there is enough amount of product in stock
                    c.shoppingCart[product.product_id] = addQuantity
                    self.setCurrentTotalShoppingCart(c)
                    return True
                else:
                    return None
    
    def sellProduct(self, c, p, q):
        #p = self.getProduct(prod_id)
        if p.quantity < q:
            return False
        else:
            quantityLeft = p.quantity - q
            p.updateStock(quantityLeft)
            c.addToHistory(p.name)
            return True

    def confirmOrder(self, c, shippingAddress, card, paymentWithBonus):
        if c.shoppingCart:                                                                      # Before we confirm the order we need to make sure that there are listed items in the shopping Cart
            total = 0
            if verifyCard(card):                # Our 'mock credit card verification' is: It needs to be 16 digits, first number needs to be even and last number needs to be odd
                placedDate = generateRandomDate()
                o = Order(shippingAddress, placedDate, placedDate+datetime.timedelta(days=2)) # We create an Order object with a random date generated in the previous line for the placed date and the delivered day 2 days after
                for prod_id, q in c.shoppingCart.items():                                    # We iterate through the shoppingCart(dictionary) items
                    p = self.getProduct(prod_id)
                    self.sellProduct(c, p, q)
                    total += self.calculatePrice(p, self.getValidCoupons(placedDate), q)         # This variable is saving the total purchase we use the output of getValidCoupons (list) as a parameter to calculate the price, cause we are only interested in the current valid coupons

                paid = total
                if paymentWithBonus:                                                        # IF statement to check if the client wants to pay with Bonus points or not
                    equivalent = c.bonus_points/10                                          # If the customer wants to pay with bonus points, we get the equivalence in euros.  1 Bonus Point = .10 Euros
                    if equivalent >= total:                                                 # If the equivalence is higher or  equal to the totalExpense, then the customer will have to pay nothing and he/she will still have some bonus points left
                        paid = 0
                        c.deleteBonusPoints(total*10)                                       # We only remove the used bonus points from the customer, cause she/he had more than needed.
                    else:                                                                   # If the equivalence is lower than the totalExpense, then the customer will just cover part of the totalExpense with his/her bonus points
                        paid -= equivalent                                                  # The paid value is the total money the customer will pay, substracting the bonus points equivalence
                        c.deleteBonusPoints(c.bonus_points)                                 # We removed the bonus points from the customer account, in this case we remove all
                temporalShoppingCart = copy.copy(c.shoppingCart)                            # We create an indepent copy of the shopping cart, because we are going to clear the variable once the order is placed

                o.placeOrder(temporalShoppingCart, total, paid)                             # We call the placeOrder method for the specific order, so that it save the purchased items and the total
                c.registerOrder(o, total)
                self.addOrderToShop(o)                                                   # We register the corresponding order to the customer, it takes as parameters the Order object and the total Expense         
                return True
            else:
                return False
        else:
            return None
    def calculatePrice(self, p, serializedCoupons, q):                                # Method to calculate the Price
        #p = self.getProduct(prod_id)
        productPrice = p.price*q
        for coup in serializedCoupons:                                                      # With this loop we check if there is any valid Coupon that can be applied to the product based on the category
            if coup["category"] == p.category:                                              # If the category of the product is the same of the coupon
                productPrice = productPrice*(1 - coup["discount"]*0.01)
                break
        return productPrice
            
    def getShopCategories(self):                                                        # This function gets all the categories we have in our shop
        availableCategories = []
        for prod in self.products:
            if prod.category not in availableCategories:
                availableCategories.append(prod.category)
        return availableCategories

    def getCustomerHistoryCategories(self, customer):                                   # This function checks which categories the user has been buying fromm
        categories = []
        c = self.getCustomer(customer.customer_id)
        for i in c.history:
            for p in self.products:
                if p.name == i:
                    if p.category not in categories:
                        categories.append(p.category)
                    break
        return categories

    def recommendationList(self, customer):
        recommendations = []
        otherCategories = copy.copy(self.getShopCategories())

        if len(self.getCustomerHistoryCategories(customer)) == 0:                                                                               # This means the Customer history is empty
            for p in self.products:
                if len(recommendations) < 10:
                    recommendations.append(p.name)                                                                          # We recommend the first 10 products of our products
        else:
            for cat in self.getCustomerHistoryCategories(customer):
                for item in self.products:
                    if item.category == cat and item not in recommendations and len(recommendations) < 10:
                        recommendations.append(item.name)
                otherCategories.remove(cat)
            otherRecommendedCategory = choice(otherCategories)

            for item in self.products:
                if len(recommendations) < 10:
                    if item.category == otherRecommendedCategory:
                        recommendations.append(item.name)
                else:
                    break
        return recommendations
 
    def addCoupon(self, coupon):
        if transformToDate(coupon.date2) and transformToDate(coupon.date1):            # First we make sure that both dates are valid
            if transformToDate(coupon.date2) > transformToDate(coupon.date1):           # We need to make sure that the final date is after the first valid date
                self.coupons.append(coupon)
                return True
            else:
                return None
        else:
            return False

    def getValidCoupons(self, placedDate):
        today = placedDate
        validCoupons = []
        for i in self.coupons:
            if today >= transformToDate(i.date1) and today <=transformToDate(i.date2):   # Is valid if the day the order was placed is between the valid dates of the coupon
                validCoupons.append(i)
        
        serializedCoupons = [MyEncoder().default(c) for c in validCoupons]   # We create a list only with the coupons that are currently valid at the moment of the purchase
        return serializedCoupons 
    
            
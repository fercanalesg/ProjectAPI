import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies

from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, Api, reqparse
from util.json_utils import ShopJsonEncoder, MyEncoder, transformToDate

from model.Customer import Customer
from api.ProductsAPI import ProductAPI
from model.data import my_shop

import datetime

import copy

app = Flask(__name__)
api = Api(app)

CustomerOrdersAPI = Namespace('customerOders', description = "", path = "/customer/<customer_id>") # If we dont specify a path, the default one will be the first parameter, but here we have specified it manually
api.add_namespace(CustomerOrdersAPI)


@CustomerOrdersAPI.route("/add2cart")
class Add2Cart(Resource):
    @CustomerOrdersAPI.doc(description = "Add an item to shopping cart",
                           params = {"product_id" : "Product ID ",
                                     "addQuantity" : "desired quantity of the product to add to the cart "})
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        args = request.args
        product_id = args["product_id"]
        addQuantity = int(args["addQuantity"])
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"No extisting product with the ID: {product_id}")
        else:
            if my_shop.addToShoppingCart(customer_id, p, addQuantity) == True:
                return jsonify(c.shoppingCart)
                #return jsonify(f"Product {product_id} added to your cart")
                """ serializedCustomers = []
                for cus in my_shop.customers:                                                        
                    temporalCustomer = copy.copy(cus)                                               # We create an independent copy of the customer because we are going to serialized the 'orders' attribute and we dont want to modify the original object                                       
                    s = MyEncoder().default(temporalCustomer)                                        
                    sOrders = [MyEncoder().default(i) for i in s["orders"]]                          
                                                                                                
                    s["orders"] = sOrders                                                            # We override the s['orders'] list with the jsonify list created in the previous line
                    serializedCustomers.append(s)                                                    # We append it to our serializedList, we are going to return it in the next line """
                #return jsonify(serializedCustomers)
            elif my_shop.addToShoppingCart(customer_id, p, addQuantity) == False:
                return jsonify("This product is not in your shoppingCart")
            elif my_shop.addToShoppingCart(customer_id, p, addQuantity) == "Not valid":
                return jsonify("Enter a valid quantity")
            else:
                return jsonify("Not enough stock of the desired product in stock")


@CustomerOrdersAPI.route("/order")
class ConfirmOrder(Resource):
    @CustomerOrdersAPI.doc(description = "Confirm an order",
                           params = {"shippingAddress" : "The shipping address of the order",
                                     "cardNumber" : "A valid Card Number",
                                     "paymentWithBonus" : "'Y' or 'N' if the customer wants to pay with their Bonus Points"})
    def post(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        args = request.args
        shipping = args["shippingAddress"]
        card = args["cardNumber"]
        if args["paymentWithBonus"].upper() == 'Y':    
            paymentWithBonus = True                                         # We create a Boolean variable to track if the customer wants to pay with bonus points or not
        else:
            paymentWithBonus = False
        
        if my_shop.confirmOrder(c, shipping, card, paymentWithBonus) == True:
            return jsonify("The order was placed successfully")
            serializedOrders = [MyEncoder().default(i) for i in c.orders]
            return jsonify(serializedOrders)
        elif my_shop.confirmOrder(c, shipping, card, paymentWithBonus) == False:   # If the card does not pass the card verification, we notify the customer and the order can not be placed 
            return jsonify("Invalid card")
        else:
            return jsonify("Your shopping Cart is empty!")

@CustomerOrdersAPI.route("/orders")
class ListOrders(Resource):
    @CustomerOrdersAPI.doc(description = "Display the list of orders from the specific customer")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        serializedOrders = [MyEncoder().default(i) for i in c.orders]
        return jsonify(serializedOrders)

@CustomerOrdersAPI.route("/returnable")
class ReturnList(Resource):
    @CustomerOrdersAPI.doc(description = "Display the list of items that can still be returned from the specific customer")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        serializedOrders = [MyEncoder().default(i) for i in c.orders]
        stillReturnable =[]
        for order in serializedOrders:
            delivered = transformToDate(order["deliveredDate"])
            if delivered + datetime.timedelta(weeks=2) >= datetime.date.today():   # If the delivered date + 2 weeks is higher or equal to today's date, the products can still be returnable, if it is lower, it means the return days are over
                stillReturnable.append(order["purchasedItems"])
        return jsonify({"The articles you can still return" : stillReturnable})

            
@CustomerOrdersAPI.route("/recommendations")
class Recommendations(Resource):
    @CustomerOrdersAPI.doc(description = "Get a list of 10 best product to be recommended based on the customer's purchase history")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("No existent customer")
        else:
            return jsonify({"Items you might be interested in: ": my_shop.recommendationList(c)})

@CustomerOrdersAPI.route("/points")
class CustomerPoints(Resource):
    @CustomerOrdersAPI.doc(description = "Return the total bonus points earned by the customer so far")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"No registered customer with ID {customer_id}")
        else:
            return jsonify ({"Customer" : customer_id, "BONUS POINTS" : c.bonus_points})

    @CustomerOrdersAPI.doc(description = "Add bonus points to the customer", 
                           params ={"extraPoints" : "How many points are we gonna add to the cosumer?"})
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"No registered customer with ID {customer_id}")
        else:
            args = request.args
            extra = int(args["extraPoints"])
            if c.addBonusPoints(extra):
                return jsonify(f"{extra} Bonus Points added to customer {customer_id}")
                #return jsonify ({"Customer" : customer_id, "BONUS POINTS" : c.bonus_points})
            else:
                return jsonify("Invalid value")
            
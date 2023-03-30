import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies

from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, Api, abort
from model.Customer import Customer
from model.Product import Product
from model.data import my_shop
from util.json_utils import JSONEncoder, MyEncoder

app = Flask(__name__)    # This is to start our Flask server
app.config["JSON_SORT_KEYS"] = False
api = Api(app)           # We make an instance of the class Api, to be able to use all the methods, it receives as a parameter an app previously created, or you can created manually with certain parameters


ProductAPI = Namespace('product', description='Product Management')   
api.add_namespace(ProductAPI)

TheProductsAPI = Namespace('products', description = "Operations with multiple products")
api.add_namespace(TheProductsAPI)


@ProductAPI.route('/')                  
                        # The resource below is going to be called whenever we enter 'product/', because as it is a route created from ProductAPI, the name of the namespaces ALWAYS goes before the specified route here in the instance
class AddProductA(Resource):                                            # A resource is something which you are interested in tracking the change of 'state' of it. In this case, we are interested in checking the state Added - Not added
    @ProductAPI.doc(description = "Add a new product to the store",     # This is pure documentation to make everything readable and understandable for a third person who is interested in getting to know our API
                    params={'name': 'Product name',
                            'price' : "Price of the product",             
                            'expiry': 'expiry date',
                            'category': 'product category',
                            'quantity' : "Amount of product that will be in stock"})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        price = float(args['price'])
        expiry = args['expiry']
        category = args['category']
        quantity = int(args['quantity'])

        new_product = Product(name, expiry, category, quantity, price)  # We create an instance of our class Product, with the specified data.

        my_shop.addProduct(new_product) # We call the method that is defined in our Shop class
        return jsonify(f"{name} succesfully added to the Shop")
       
    
    
@ProductAPI.route('/<product_id>')
class SpecificCustomerOps(Resource):

    @ProductAPI.doc(description = "Return the data of the product with the specified customer id")
    def get (self, product_id):     # The product_id variable is taken from the route
        product_search = my_shop.getProduct(product_id)
        if not product_search:      # We check if the product with the given id actually exists in our shop
            return jsonify(f"No existing product with the ID {product_id}")
        else:
            return MyEncoder().default(product_search)  # As we want to return the class object as serialized data (dict), we pass it through our JSONEncoder class

    @ProductAPI.doc(decription = "Delete an existing product")
    def delete(self, product_id):
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"No existing product with the ID {product_id}")
        my_shop.deleteProduct(p)
        return jsonify(f"Product with ID {product_id} was removed")
            

    @ProductAPI.doc(decription = "Change the stock of an existing product",
                    params = {"quantity":"Available stock of the product"})
    def put(self, product_id):
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"Not existing product with the ID {product_id}")
        else:
            args = request.args
            quantity = int(args["quantity"]) # The type of variable retrieved from the request is str, so we transform it into integer
            if p.updateStock(quantity):
                return jsonify("Product stock has been updated")
            else:
                return jsonify("Invalid quantity")


@ProductAPI.route('/sell')
class SellProduct(Resource):
    @ProductAPI.doc(description = "Sell a product",
                    params = {"customer_id" : "Customer ID",
                              "product_id" : "Product ID",
                              "sold_quantity" : "Quantity of product sold"})
    
    def put(self):
        args = request.args
        sold_quantity = int(args["sold_quantity"])
        product_id = args["product_id"]
        customer_id = args["customer_id"]
        p = my_shop.getProduct(product_id)
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"Not registered customer with ID {customer_id}")
        if not p:
            return jsonify(f"Not registered product with ID {product_id}")

        if my_shop.sellProduct(c, p, sold_quantity) == False:    # If the desired buying quantity is higher than the available stock of the specific product, we can not proceed to sell it
            return jsonify("Not enough amount of this product to sell")
        else:
            """ quantityLeft = p.quantity - sold_quantity
            p.updateStock(quantityLeft)
            c.addToHistory(p.name) """
            #print(f"Agregado {p.name}")
        serializedProducts = [MyEncoder().default(i) for i in my_shop.products]  # We use the override method 'default()' from the class we created (MyEncoder) to serialize each of the elements of the list, at the same time we serialize them, we save them in a list. 
        return jsonify(serializedProducts)
        #return jsonify("Enjoy the product!!") 



@ProductAPI.route('/remove')
class RemoveProduct(Resource):
    @ProductAPI.doc(description = "Removing a product from the inventory, not deleting it",
                    params = {"product_id" : "The ID of the product we want to remove",
                              "reason" : "The reason for the product removal"})
    def put(self):
        args = request.args
        product_id = args["product_id"]
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify(f"Not registered product  with ID {product_id}")
        else:
            reason = args["reason"]
            my_shop.removeProduct(p, reason)  
            return jsonify("Product stock was succesfully removed from inventory")    
        

@TheProductsAPI.route('/')
class ProductsData(Resource):
    def get(self):
        if  len(my_shop.products) != 0:                             # We check that there are already some registered customers
            serializedProducts = [MyEncoder().default(i) for i in my_shop.products]  # We use the override method 'default()' from the class we created (MyEncoder) to serialize each of the elements of the list, at the same time we serialize them, we save them in a list. 
            return jsonify(serializedProducts)                                        # Once we have our list with serialized data, we can simply just jsonify it to get our result in a json format
        abort(500, "Currently there are no registered products!")

@TheProductsAPI.route('/reorder')
class ReorderProduct(Resource):
    @TheProductsAPI.doc(description = "Show a list of the productst that need to be reorder")
    def get(self):
        if my_shop.reorderList() != False:
            return jsonify(my_shop.reorderList())
        else:
            return jsonify("None product needs to be reorder")


""" if __name__ == "__main__":
    app.run(debug=True) """
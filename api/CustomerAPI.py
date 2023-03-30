import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies

from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, Api, reqparse, abort

from model.Customer import Customer
from model.data import my_shop
from util.json_utils import ShopJsonEncoder, MyEncoder

import copy

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False # This is so that once we return our jsonify data, it keeps the original order
api = Api(app)

CustomerAPI = Namespace('customer', description='Customer Management')         # A Namespace is used to wrap multiple endpoints, which are going to share a base route, in this case, 
                                                                               # we are going to wrap all the endpoints related to the methods we want to perform in our Customers
api.add_namespace(CustomerAPI)

""" PruebaName = Namespace("prueba", description = "Understandind Namespaces")
api.add_namespace(PruebaName)

@PruebaName.route("/pruebame")
class Probando(Resource):
    def get(self):
        return "Mi prueba" """
    

@CustomerAPI.route('/')                                              # The resource below is going to be called whenever we enter 'customer/', because as it is a route created from CostumerAPI, the name of the namespaces ALWAYS goes before the specified route here in the instance
class GeneralCustomerOps(Resource):                                  # A resource is something which you are interested in tracking the change of 'state' of it. In this case, we are interested in checking the state of Customers (the number of customers and which they are)
    @CustomerAPI.doc(description="Get a list of all customers")      # This is pure documentation to make everything readable and understandable for a third person who is interested in getting to know our API, you put if before calling the HTTP method function
    def get(self):                                                   # As the class inherits from 'Resource' we can make use of the HTTP methods simply naming the function same as the method and it will understand it. 
                                                                     # If we would like to put another name to the function, we need to specify in the route(), the methods we will be using as parameter methods = ["GET", "POST"]
        
        if  len(my_shop.customers) != 0:                                                # We check that there are already some registered customers                                        
            serializedCustomers = []
            for cus in my_shop.customers:                                               # With this for loop we are going to transform each of the objects into a __dict__ format to be able to return them, but we are creating a copy of them, because we don't want to modify the original ones
                temporalCustomer = copy.copy(cus)                                       # We are creating a copy of the object, but it is not sharing reference, it is completely independent, so that we don't modify the original object
                s = MyEncoder().default(temporalCustomer)                               # This variable is saving each of the customers as a key-value format
                sOrders = [MyEncoder().default(i) for i in s["orders"]]                 # Once we have the object Customer in a dictionary format, we know that the key "orders" is a list, a list of objects from the ORDER class                                                                    # So what we basically do is, each of the object in the 'orders' list, we transform it into a __dict__ format, so that it can me jsonify later on and we can be able to return it through the request
                                                                                        # We use the override method 'default()' from the class we created (MyEncoder) to serialize each of the elements of the list, at the same time we serialize them, we save them in a list.

                s["orders"] = sOrders                                                   # We override the s['orders'] list with the jsonify list created in the previous line
                serializedCustomers.append(s)                                           # We append it to our serializedList, we are going to return it in the next line                                                                                        
            return jsonify(serializedCustomers)                                         # Once we have our list with serialized data, we can simply just jsonify it to get our result in a json forma
        abort(500, "Currently there are no registered customers!")               # We send this abort message in case we dont have any registered customer to display
    
    @CustomerAPI.doc(
        description="Register a new customer",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def post(self):
        # get the post parameters, we use this method if we are passing the values in the url, with the ?key=value& format
        args = request.args   # request.args stores all the arguments that were passed through the url to the corresponding request.
        name = args['name']   # We are retrieving the values stored on each of the arguments that we passed through the url of the request       
        email = args['email']
        address = args['address']
        dob = args['dob']

        # We use this method if the post request we are making is through a json format, this way we retrieve the request with key-value
        """ name = request.json["name"]
        email = request.json["email"]
        address = request.json["address"]
        dob = request.json["dob"] """

        new_customer = Customer(name, email, address, dob)
        # add the customer
        if my_shop.addCustomer(new_customer):
            temporalCustomer = copy.copy(new_customer)                                                
            s = MyEncoder().default(temporalCustomer)                                        
            sOrders = [MyEncoder().default(i) for i in s["orders"]]                                                                                         
            s["orders"] = sOrders
            return jsonify(s)
        else:
            return jsonify("Customer with the email address already exists")


@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(description="Get data about a particular customer")
    def get(self, customer_id):    # When we pass a parameter to our CRUD method, it takes it from the route (<>), so it needs to have the same name
        search_result = my_shop.getCustomer(customer_id)
        if not search_result:                             
            return jsonify(f"No existing Customer with the ID {customer_id}")
        else:
            temporalCustomer = copy.copy(search_result)                                                
            s = MyEncoder().default(temporalCustomer)                                        
            sOrders = [MyEncoder().default(i) for i in s["orders"]]                                                                                         
            s["orders"] = sOrders
            return jsonify(s)


    @CustomerAPI.doc(description="Delete an existing customer")
    def delete(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"Customer ID {customer_id} was not found")
        my_shop.removeCustomer(c)
        return jsonify(f"Customer with ID {customer_id} was removed")


    @CustomerAPI.doc(description="Update customer data",
                     params = {"name" : "Customer Name",
                               "bonus_points" : "Customer bonus points",
                               "address" : "Customer shipping address",
                               "status" : "Customer current status",
                               'dob': 'Customer birthday'
                               })
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"Customer ID {customer_id} was not found")
        else:
            args = request.args
            
            """ name = args['name'] 
            address = args['address']
            dob = args['dob']
            status = args["status"]
            bonus_points = int(args['bonus_points']) """

            name = args['name'] if "name" in args else c.name              # If one of the parameters does not exist i.e the user does not want to change it, so we assign the value that the customer already has
            address = args['address'] if "address" in args else c.address
            dob = args['dob'] if "dob" in args else c.dob
            status = args["status"] if "status" in args else c.status
            bonus_points = int(args['bonus_points']) if "bonus_points" in args else c.bonus_points  # The data is retrieved as str so we transform it into integer """

            if c.editCustomer(name, address, dob, status, bonus_points):
                return MyEncoder().default(c)
            else:
                return jsonify("Invalid inputs")


@CustomerAPI.route('/verify')
class CustomerVerfication(Resource):
    @CustomerAPI.doc(
        description="Verify customer email address",
        params={'token': 'Verification Token sent by email',
                'email': 'Customer Email'})
    def put(self):
        args = request.args
        token = args['token']
        email = args['email']
        customer = my_shop.getCustomerbyEmail(email) 
        if customer is None:                           # If the getCustomerbyEmail method does not return anything
            return jsonify("Customer not found.")
        if customer.verify(token): 
            return jsonify(f"Customer {customer.customer_id} is now Verified!")
        else:
            return jsonify("Invalid token.")


@CustomerAPI.route('/pwreset')
class CustomerPWReset(Resource):

    @CustomerAPI.doc(
        description="Generate a temporary password and send via email.",
         params = {"customer_id" : "The customer ID"} )
    def post(self):
        args = request.args
        id = args["customer_id"]
        c = my_shop.getCustomer(id)
        if not c:                                                  # First we make sure that the Customer with the given ID exists
            return jsonify(f"No registered customer with ID {id}")
        else:
            c.generateTempPass()                                   # We call the method that is defined inside the Customer class
            return jsonify("Your temporary password has been sent to your email")
            #serializedCustomers = [MyEncoder().default(i) for i in my_shop.customers]  # We use the override method 'default()' from the class we created (MyEncoder) to serialize each of the elements of the list, at the same time we serialize them, we save them in a list. 
            #return jsonify(serializedCustomers)

    @CustomerAPI.doc(
        description="Allow password reset based on the temporary password",
        params={'customer_id' : "The customer ID",
                'temp_pw': 'Password sent by email',
                'new_pw': 'New password'})
    def put(self):
        args = request.args
        id = args["customer_id"]
        temp_pw = args["temp_pw"]
        new_pw = args["new_pw"]
        c = my_shop.getCustomer(id)
        if not c:
            return jsonify(f"No registered customer with ID {id}")
        else:
            if c.resetPass(temp_pw,new_pw) != False:                           
                return jsonify("Your password has succesfully been saved")
                #serializedCustomers = [MyEncoder().default(i) for i in my_shop.customers]  # We use the override method 'default()' from the class we created (MyEncoder) to serialize each of the elements of the list, at the same time we serialize them, we save them in a list. 
                #return jsonify(serializedCustomers)
            else:
                return jsonify("Wrong temporary passsword, please try again")


""" if __name__ == "__main__":
    app.run(debug=True) """
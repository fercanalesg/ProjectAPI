import sys, os
thepath = os.getcwd(); sys.path.append(thepath) # 'thepath' saves the current directory. We append that path to sys, because here is where it is going to look for dependencies, and we are adding our current directory

from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, Api
import datetime

#from model.Customer import Customer
#from model.Product import Product
from model.Coupon import Coupon

from model.data import my_shop
from util.json_utils import ShopJsonEncoder, MyEncoder, transformToDate

from api.CustomerAPI import CustomerAPI                   # We import the Namespaces we created in the other files, to be able to use all the methods
from api.ProductsAPI import ProductAPI, TheProductsAPI
from api.OrdersAPI import CustomerOrdersAPI


superShopApp = Flask(__name__)
superShopApp.config["JSON_SORT_KEYS"] = False # This is so that once we return our jsonify data, it keeps the original order
#superShopApp.json_encoder = ShopJsonEncoder
api = Api(superShopApp, version='1.0', title='SuperShopManager',
                   contact_email = "22IMC30051@fh-krems.ac.at",
                   description='Shop Management API')


Coupons = Namespace("coupons", description = "Management of festival and weekend sales discounts")
api.add_namespace(Coupons)
api.add_namespace(CustomerAPI)
api.add_namespace(ProductAPI)
api.add_namespace(TheProductsAPI)
api.add_namespace(CustomerOrdersAPI)


@Coupons.route("")
class CouponsOps(Resource):
    @Coupons.doc(description = "Get a list of all currently valid coupons")
    def get(self):
        return jsonify(my_shop.getValidCoupons(datetime.date.today()))

    @Coupons.doc(description = "Add a new coupon for a product category",
                 params = {"category" : "To which products category is the discount going to be applied",
                           "discount" : "How much the discount will be?",
                           "date1" : "First date of validity",
                           "date2" : "Last day of validity"})
    def post(self):
        args = request.args
        category = args["category"]
        discount = args["discount"]
        date1 = args["date1"]
        date2 = args["date2"]
        coupon = Coupon(date1, date2, discount, category)
        if my_shop.addCoupon(coupon) == False:
            return jsonify("Invalid dates")
        elif my_shop.addCoupon(coupon) == None:
            return jsonify("The validity range of the coupon is not valid")
        else:
            return (MyEncoder().default(coupon))


if __name__ == "__main__":
    superShopApp.run(debug=True, port=7890)

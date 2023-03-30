import datetime

import pytest
from model.Customer import Customer
from model.Product import Product
from model.Shop import Shop
from model.Coupon import Coupon
from model.Order import Order
from util.json_utils import verifyCard

@pytest.fixture()
def initShop():
    my_shop = Shop()
    return my_shop

@pytest.fixture()
def generateCustomer():
    c1 = Customer("Fernando Navarro", "lufercanalesg@gmail.com", "Viena 123", "30.9.2000")
    c2 = Customer("John Winston", "testingg@gmail.com", "Chicago 156", "10.9.2003")
    c3 = Customer("Emily Davis", "emilydavis@hotmail.com", "Dubai 812", "29.04.1988")
    c4 = Customer("Kate Tant", "katherinentnt@gmail.com", "St Polten 123", "12.2.2000")
    c5 = Customer("Natalia Serrato", "nataliaserratg@gmail.com", "Mexico 152", "14.2.1998")
    c6 = Customer("Paul Walker", "paulwalker@gmail.com", "California 198", "7.1.2008")
    c7 = Customer("Martha Lee", "sarahlee@gmail.com", "USA 657", "14.02.1995")
    c8 = Customer("Lisa Phanton", "lisatest@gmail.com", "Finland 728", "3.7.2006")
    c9 = Customer("Adam Brown", "adambrown@hotmail.com", "Salzburg 125", "05.03.1980")
    c10 = Customer("Karen Lee", "karenlee@gmail.com", "Budapest 820", "28.06.1991")

    return [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]

@pytest.fixture()
def generateProducts():
    p1 = Product("Apple", "12.04.2023", "Fruits", 40, 2)
    p2 = Product("Bananas", "02.04.2023", "Fruits", 8, 1.5)
    p3 = Product("Watermelon", "20.04.2023", "Fruits", 17, 5)
    p4 = Product("Blueberries", "15.04.2023", "Fruits", 7, 3)
    p5 = Product("Peaches", "20.04.2023", "Fruits", 42, 2.99)
    p6 = Product("Orange", "20.04.2023", "Fruits", 90, 3)
    p7 = Product("Pineapple", "26.04.2023", "Fruits", 8, 5)
    p8 = Product("Grapes", "15.04.2023", "Fruits", 7, 3.50)
    p9 = Product("Fish", "03.04.2023", "Meat", 18, 11)
    p10 = Product("Bacon", "31.03.2023", "Meat", 9, 7)
    p11 = Product("Chicken Breast", "13.04.2023", "Meat", 25, 12)
    p12 = Product("Lamb", "02.04.2023", "Meat", 2, 10)
    p13 = Product("Steak", "3.04.2023", "Meat", 15, 10)
    p14 = Product("Sausages", "10.04.2023", "Meat", 4, 7)
    p15 = Product("Salmon", "08.04.2023", "Meat", 2, 12.75)
    p16 = Product("Sour Cream", "30.03.2023", "Dairy", 2, 6)
    p17 = Product("Yogurt", "1.04.2023", "Dairy", 20, 4)
    p18 = Product("Cheese", "01.05.2023", "Dairy", 19, 6)
    p19 = Product("Eggs", "01.04.2023", "Dairy", 12, 2)
    p20 = Product("Butter", "05.04.2023", "Dairy", 4, 2.75)
    p21 = Product("Cheddar Cheese", "29.04.2023", "Dairy", 9, 7)
    p22 = Product("Corn", "01.04.2023", "Vegetables", 12, 3)
    p23 = Product("Broccoli", "05.04.2023", "Vegetables", 22, 4)
    p24 = Product("Potatoes", "10.04.2023", "Vegetables", 70, 2.25)
    p25 = Product("Spinach", "23.04.2023", "Vegetables", 5, 3)
    p26 = Product("Cabbage", "05.04.2023", "Vegetables", 3, 1.50)
    p27 = Product("Peas", "03.04.2023", "Vegetables", 40, 2)
    p28 = Product("Tomatoes", "01.04.2023", "Vegetables", 33, 3)
    p29 = Product("All Bran", "15.08.2023", "Cereals/Bars", 50, 3)
    p30 = Product("Captain Crunch", "31.12.2023", "Cereals/Bars", 25, 6)
    p31 = Product("Lucky Charms", "25.10.2023", "Cereals/Bars", 50, 6)
    p32 = Product("Oreo", "30.11.2023", "Cereals/Bars", 14, 8)
    p33 = Product("Oats", "8.07.2023", "Cereals/Bars", 60, 4.5)
    p34 = Product("Rice Cakes", "1.10.2023", "Cereals/Bars", 34, 3)
    p35 = Product("Donut", "2.04.2023", "Bakery", 12, 2.5)
    p36 = Product("Baguette", "05.04.2023", "Bakery", 15, 1.50)
    p37 = Product("Carrot Cake", "02.05.2023", "Bakery", 19, 3.40)
    p38 = Product("Bisquet", "4.04.2023", "Bakery", 14, 1.5)
    p39 = Product("Apfelstrudel", "6.04.2023", "Bakery", 5, 4.5)
    p40 = Product("Croissant", "29.06.2023", "Bakery", 9, 2)

    return[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
             p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
             p21, p22, p23, p24, p25, p26, p27, p28, p29, p30,
             p31, p32, p33, p34, p35, p36, p37, p38, p39, p40]
@pytest.fixture()
def generateCoupons():
    coup1 = Coupon("11.04.2022", "25.07.2022", 15, "Fruits")
    coup2 = Coupon("23.02.2023", "15.05.2023", 3, "Meat")                # Currently Valid
    coup3 = Coupon("24.06.2023", "24.07.2023", 20, "Meat")
    coup4 = Coupon("2.05.2023", "13.06.2023", 10, "Cereals/Bars")
    coup5 = Coupon("7.03.2023", "14.07.2023", 5, "Dairy")                # Currently valid
    coup6 = Coupon("2.09.2022", "30.11.2022", 10, "Fruits")

    return [coup1, coup2, coup3, coup4, coup5, coup6]

@pytest.fixture()
def generateOrders():
    o1 = Order("Bahnhofplatz 16", "29.3.2023", "31.3.203")
    o2 = Order("Vienna 810", "1.04.2023", "3.04.2023")
    o3 = Order("Paris 924", "10.04.2023", "12.04.2023")
    return [o1,o2,o3]

def test_AddRemoveCustomers(initShop, generateCustomer):
    for i in generateCustomer:
        initShop.addCustomer(i)
    assert len(initShop.customers) == 10                 # We test if all customers are now in the list
    assert generateCustomer[1] in initShop.customers    # We check if an specific customer is in the list

    initShop.removeCustomer(generateCustomer[2])
    assert len(initShop.customers) == 9                  # We test that the list has now one less Customer
    initShop.addCustomer(generateCustomer[0])
    assert len(initShop.customers) == 9                  # We test that the action above was not executed, because the customer already exists

def test_editCustomer(initShop, generateCustomer):
    c = generateCustomer[4]
    initShop.addCustomer(c)
    assert c.name == "Natalia Serrato"
    assert c.editCustomer("Fernando", "Bahamas 719", "89.9999.1000", "Verified", 56) == False       # It has an invalid dob date

    c.editCustomer("Fernando", "Bahamas 719", "30.09.2000", "Verified", -104)                       # Bonus points parameter is not valid
    assert c.name == "Natalia Serrato"                                                              # This is a test to check that the customer has not been edited due to previous invalid entries

    c.editCustomer("Fernando", "Bahamas 719", "15.9.1996", "Verified", 45)                          # Valid parameters
    assert c.name == "Fernando"                                                                     # The name and the address have been successfully modified
    assert c.address == "Bahamas 719"


def test_verifyCustomer(initShop, generateCustomer):
    c1, c2 = generateCustomer[1], generateCustomer[2]
    initShop.addCustomer(c1)
    initShop.addCustomer(c2)
    assert c1.status == "unverified"            # The customer status is set to 'unverified' when it is registered
    verToken1 = c1.verification_token
    c1.verify(verToken1)
    assert c1.status == "verified"              # We test that the customer1 is verified, because we used the correct verification token

    c2.verify("notVerificationToken")
    assert c2.status == "unverified"            # We test that the customer2 is not verified, we used a wrong token

def test_changePassword(initShop, generateCustomer):
    c4 = generateCustomer[4]
    initShop.addCustomer(c4)
    c4.generateTempPass()
    assert c4.tempPass != None                             # The user has now a temporary Password, it has been sent to his email

    temporary = c4.tempPass
    c4.resetPass("ThisIsNotTheTempPass", "MyNewPassword")
    assert c4.tempPass != None                              # The user should still have a temporary password because it hasn't reset it yet, he didn't use the correct temmporary password

    c4.resetPass(temporary, "MyNewPassword")
    assert c4.tempPass == None
    assert c4.newPass == "MyNewPassword"                    # Now the password has been changed and the temporary password was deleted


def test_AddRemoveProducts(initShop, generateProducts):
    newprod = Product("Carrot", "9.05.2023", "Vegetables", 67, 2)
    for i in generateProducts:
        initShop.addProduct(i)
    assert len(initShop.products) == 40                 # We test if all products are now in the list
    initShop.removeProduct(generateProducts[0], "The product was expired")
    assert generateProducts[0] in initShop.products       # This product is still in the list of items, because we just deleted stock from the inventory but not Deleted the product
    assert generateProducts[0].quantity == 0

    initShop.deleteProduct(generateProducts[3])
    assert generateProducts[3] not in initShop.products   # We test that the product is no longer in the list of the shop
    initShop.addProduct(newprod)
    assert len(initShop.products) == 40                   # We add a new product and we check that the length of the list is again 40


@pytest.mark.parametrize("quantity, output",                                 # Multiple possible entries for updating quantity of stock
                         [
                             (146, True),
                             ("-100", False),                               # Negative numbers are not valid
                             (23, True),
                             ("notvalidentry", False),                      # No integers
                             ("*#$%^", False)                               # Characters are not accepted


                         ])
def test_updateStock(initShop, quantity, output):
    myprod = Product("Celery", "12.04.2023", "Vegetables", 30, 5)
    initShop.addProduct(myprod)

    myprod.updateStock(80)
    assert myprod.quantity == 80  # We check that the stock was correctly updated

    assert myprod.updateStock(quantity) == output


def test_addingToCart(initShop, generateCustomer, generateProducts):
    for c, p in zip(generateCustomer, generateProducts):
        initShop.addCustomer(c)
        initShop.addProduct(p)
    c1 = generateCustomer[8]
    p1 = generateProducts[0]  # Product("Apple", "12.04.2023", "Fruits", 40, 2)
    p2 = generateProducts[1]  # Product("Bananas", "02.04.2023", "Fruits", 8, 1.5)
    assert c1.currentTotalShoppingCart == 0                                             # customer current total shopping cart should be 0 because it does not have any items on it

    initShop.addToShoppingCart(c1.customer_id, p1, 50)
    assert len(c1.shoppingCart) == 0                                                    # customer 1 shopping cart should be empty, because is trying to add a higher amount that the one available in stock (40)

    initShop.addToShoppingCart(c1.customer_id, p1, 25)
    assert p1.product_id in c1.shoppingCart                                             # item p1 should be in the shopping cart now

    initShop.addToShoppingCart(c1.customer_id, p2, 5)
    assert p2.product_id in c1.shoppingCart
    assert c1.currentTotalShoppingCart == (p1.price*25 + p2.price*5)                   # now the current total shopping cart should be the sum of the products multiplied by their prices

    initShop.addToShoppingCart(c1.customer_id, p1, -1)
    assert p1.product_id not in c1.shoppingCart                                        # We check that the product is removed from the shopping cart
    assert c1.currentTotalShoppingCart == p2.price*5
    initShop.addToShoppingCart(c1.customer_id, p2, -1000)
    assert p2.product_id in c1.shoppingCart                                             # As we gave an invalid input, the product is still in the shopping cart

@pytest.mark.parametrize("card, output",                                 # Multiple possible entries for the card verification
                         [
                             ("1222443529427367", False),                # First number is not even
                             ("cardNumber", False),                       # There are no numbers
                             ("2387729450187657", True),                 # Valid cardNumber
                             ("456189", False),                            # Not 16 digits
                             ("2912643368329344", False),                   # Las number is not odd
                             ("4739889374657991",True),                    # Valid cardNumber
                             ("*CARD NUMBER/-#", False)                            # Invalid entry
                         ])
def test_validCard(card, output):
    assert verifyCard(card) == output


def test_confirmOrder(initShop, generateCustomer, generateProducts, generateCoupons):
    for c,p in zip(generateCustomer, generateProducts):
        initShop.addCustomer(c)
        initShop.addProduct(p)

    initShop.addToShoppingCart(generateCustomer[0].customer_id, generateProducts[0], 4)
    assert len(generateCustomer[0].history) == 0                                                        # We are testing that at this point the customer history is empty because he hasn't confirmed any order yet

    initShop.confirmOrder(generateCustomer[0], "Vienna 143", "2348376789209877", True)
    assert generateProducts[0].quantity == 36                                                          # The stock of the product is updated in the store

    assert len(generateCustomer[0].orders) == 1
    # assert len(generateCustomer[0].history) == 2

def test_sellProduct(initShop, generateCustomer,generateProducts):
    my_shop = initShop
    c1 = generateCustomer[3]
    my_shop.addCustomer(c1)
    p1 = generateProducts[20]  # Product("Cheddar Cheese", "29.04.2023", "Dairy", 9, 7)
    p2 = generateProducts[21]  # Product("Corn", "01.04.2023", "Vegetables", 12, 3)
    my_shop.addProduct(p1)
    my_shop.addProduct(p2)

    assert len(c1.history) == 0                         # The customer's history is empty
    my_shop.sellProduct(c1, p1, 5)
    assert p1.name in c1.history                        # Now the customer's history contains the product we sold
    assert p1.quantity == 4                             # The available stock of that product is updated too

    my_shop.sellProduct(c1, p2, 20)
    assert len(c1.history) == 1                         # The product in the line above was not added, because we are tryin to sell a higher amount than the one available in stock(12)



@pytest.mark.parametrize("coupons, outputs",                                                        # Multiple possible entries for adding a coupon
                         [
                             (Coupon("30.05.2023", "26.3.2022", 50, "Meat"), None),                       # Invalid, the final date of the coupon needs to be after the start date
                             (Coupon("572.invalid*date", "92036438", 30, "Bakery"), False),                 # Invalid, not valid format for the dates
                             (Coupon("15.05.2023", "20.05.2023", 7, "Cereals/Bars"), True)
                            ])
def test_addCoupons(initShop, coupons, outputs):
    coup1 = Coupon("23.04.2023", "28.05.2023", 15, "Fruits")
    initShop.addCoupon(coup1)
    assert len(initShop.coupons) == 1                                       # We test that the coupon was successfully added
    assert initShop.addCoupon(coupons) == outputs

def test_getValidCoupons(initShop, generateCoupons):
    for coup in generateCoupons:
        initShop.addCoupon(coup)
    assert len(initShop.getValidCoupons(datetime.date.today())) == 2                                    # Only 2 of the coupons we created are currently valid



@pytest.mark.parametrize("products, output",                                                        # Multiple products to test the value
                         [
                             (Product("Grapes", "15.04.2023", "Fruits", 7, 3.50), 6.3),
                             (Product("Fish", "03.04.2023", "Meat", 18, 11), 22),                   # None coupon applied
                             (Product("Cheddar Cheese", "29.04.2023", "Dairy", 9, 7), 14),          # None coupon applied
                             (Product("Corn", "01.04.2023", "Vegetables", 12, 3), 6),               # None coupon applied
                             (Product("Orange", "20.04.2023", "Fruits", 90, 3), 5.4),
                             (Product("Pineapple", "26.04.2023", "Fruits", 8, 5), 9)
                            ])

def test_calculatePrice(initShop, products, output, generateCoupons):

    coup1 = Coupon("28.03.2023", "30.04.2023", 10, "Fruits")
    initShop.addCoupon(coup1)
    coupons = initShop.getValidCoupons(datetime.date.today())
    assert initShop.calculatePrice(products, coupons, 2) == output  # We simulate selling 2 items from each product, and only the products which are from the category "Fruits" should get a discount.

@pytest.mark.parametrize("bonus, output",                                 # Multiple possible entries for the bonus points
                         [
                             (34, True),                       # Valid
                             ("***", False),                       # No characters accepted
                             ("-24", False),                 # No negative numbers accepted
                             ("Hello", False),                            # No characters accepted
                             (100, True),                   # Valid

                            ])
def test_addBonusPoints(initShop, generateCustomer, bonus, output):
    initShop.addCustomer(generateCustomer[5])
    assert generateCustomer[5].bonus_points == 0

    generateCustomer[5].addBonusPoints(10)
    assert generateCustomer[5].bonus_points == 10                    # The points are added to the customer

    generateCustomer[5].addBonusPoints(-7)                           # You can not add negative numbers
    assert generateCustomer[5].bonus_points == 10

    assert generateCustomer[5].addBonusPoints(bonus) == output        # We test different inputs for the bonus entry

def test_placeAndRegisterOrder(initShop, generateCustomer, generateProducts, generateOrders):
    shop = initShop
    c1 = generateCustomer[5]
    shop.addCustomer(c1)
    p1 = generateProducts[1]
    p2 = generateProducts[2]
    p3 = generateProducts[3]
    shop.addProduct(p1)
    shop.addProduct(p2)
    shop.addProduct(p3)

    shop.addToShoppingCart(c1.customer_id, p1, 5)           # We add products to the shopping cart
    shop.addToShoppingCart(c1.customer_id, p2, 2)
    assert len(c1.shoppingCart) == 2                        # The customer should have already two items in his shopping cart

    o1 = generateOrders[0]                                  # We create an individual order
    assert o1.totalExpense == 0                             # The order has not being placed, this means does not contain anything

    o1.placeOrder(c1.shoppingCart, 60, 60)                  # We place the order with the shopping cart from c1
    assert len(o1.purchasedItems) == 2                      # The order should contain now 2 items
    assert c1.bonus_points == 0                             # We test that the customer has 0 bonus points because none order has been registered to his account

    c1.registerOrder(o1, 60)
    assert len(c1.shoppingCart) == 0                        # After the customer register his/her order, the shopping cart must be wiped
    assert c1.bonus_points == 60                            # The customer should have now 60 points, which is equivalent to the euros he/she spent in the registered order
    assert c1.currentTotalShoppingCart == 0                     # As the shopping cart is clean now, the current total is set to 0




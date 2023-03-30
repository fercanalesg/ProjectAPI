# the instance of shop, where all data is stored.
import os
import sys
thepath = os.getcwd(); sys.path.append(thepath) 

from model.Customer import Customer
from model.Shop import Shop
from model.Product import Product 
from model.Coupon import Coupon
from flask import jsonify


my_shop = Shop()

# Test data
c1 = Customer("Carlos Alberto", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
c2 = Customer("Fernando Canales", "lufercanalesg@email.test", "1459 Mexico", "30.01.2005")
c3 = Customer("Wero Velazquez", "werozlwsquez@gmail.com", "5191 Casiopea", "25.07.2000" )
c4 = Customer("Kate Tant", "katherinentnt@gmail.com", "St Polten 123", "12.2.2000")
c5 = Customer("Natalia Serrato", "nataliaserratg@gmail.com", "Mexico 152", "14.2.1998")
c6 = Customer("Paul Walker", "paulwalker@gmail.com", "California 198", "7.1.2008")
c7 = Customer("Martha Lee", "sarahlee@gmail.com", "USA 657", "14.02.1995")
c8 = Customer("Lisa Phanton", "lisatest@gmail.com", "Finland 728", "3.7.2006")
c9 = Customer("Adam Brown", "adambrown@hotmail.com", "Salzburg 125", "05.03.1980")
c10 = Customer("Karen Lee", "karenlee@gmail.com", "Budapest 820", "28.06.1991")
customers = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]


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

prods  = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,
           p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
           p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,
           p31,p32,p33,p34,p35, p36, p37,p38,p39,p40]


co1 = Coupon("20.03.2022", "20.05.2023", 25, "Fruits")
co2 = Coupon("28.02.2023", "12.06.2023", 90, "Fresh Food")
co3 = Coupon("3.01.2022", "23.03.2023", 15, "Electronics")
coups = [co1,co2,co3]


for i in customers:
    my_shop.addCustomer(i)

for i in prods:
    my_shop.addProduct(i)

for i in coups:
    my_shop.addCoupon(i)


print("--CUSTOMERS--")
for i in my_shop.customers:
    print(i)

print("\n")

print("--PRODUCTS--")
for i in my_shop.products:
    print(i)
print("\n")

print("--COUPONS--")
for i in my_shop.coupons:
    print(i)

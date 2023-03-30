from datetime import date, timedelta
from random import choice
from dateutil.parser import parse
from json import JSONEncoder


class ShopJsonEncoder(JSONEncoder):
    # You may need to adapt this class to deal with different type of objects 
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        # default json encoding using the __dict__
        return obj.__dict__

class MyEncoder(JSONEncoder):     # We are going to use MyEncoder to deal with different type of objects and be able to display them and send them as  responses of requests.
    def default(self, obj):    # This override function takes an object of a class as parameter
        return obj.__dict__    # It returns the 'dictionary' format of the object


def transformToDate(string):
    try:                            # This is a try-except block to check if the string we are trying to pass could be represented as a datetime object, 
        parse(string)               # parse function helps us to parse the string and check if it could be a date

        if '-' in string:                                             # If the format is in year-month-day
            dateSplit = [int(i) for i in string.split('-')]
            thedate = date(dateSplit[0],dateSplit[1],dateSplit[2])
            return thedate
        else:
            dateSplit = [int(i) for i in string.split('.')] # We split the string given in "day.month.year" format, and from the obtained list, we convert each element into integer
            thedate = date(dateSplit[2],dateSplit[1],dateSplit[0]) # We transform it into a date object so that we can be able to compare them, date(year, month, day)
            return thedate
    except ValueError:
        return False

def generateRandomDate():                           # Function to generate a random Date from 22 days before to the current date
     today = date.today() - timedelta(days=2)
     dBefore = today - timedelta(days=5)  # Original value 20
     dates = []                                      # We create a list of dates between these to dates
     while dBefore != today:
        dBefore += timedelta(days=1)
        dates.append(dBefore)
     randomDate = choice(dates)                      # We pick a random date to assign it as the placed date to test our requests
     return randomDate

def verifyCard(card):
    if len(card) == 16 and int(card[0]) % 2 == 0 and int(card[-1]) % 2 != 0:    # Our 'mock credit card verification' is: It needs to be 16 digits, first number needs to be even and last number needs to be odd
        return True
    else:
        return False

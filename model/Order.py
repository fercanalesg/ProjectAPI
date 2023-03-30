
class Order():
    def __init__(self, shippingAddress, placedDate, deliveredDate):
        self.shippingAddress = shippingAddress
        self.placedDate = str(placedDate)
        self.deliveredDate = str(deliveredDate)
        self.purchasedItems = {}
        self.totalExpense = 0          # The total amount of the purchase
        self.paid = 0                  # The real amount the customer pays (less in case he/she decides to use Bonus Points for payment)
    
    def placeOrder(self, items, total, paid):
        self.purchasedItems = items
        self.totalExpense = total
        self.paid = paid
    
    def __repr__(self) -> str:
        return f"{self.purchasedItems} - {self.totalExpense} - {self.deliveredDate}"
    
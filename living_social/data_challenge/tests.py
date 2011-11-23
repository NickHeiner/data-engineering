"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data_challenge.views import parseAndSave, getRevenue
from data_challenge.models import Customer, Item, Merchant, Transaction

class SimpleTest(TestCase):
    def test_save(self):
        name = "Snake Plissken"
        description = "$10 off $20 of food"
        price = 10.3
        quantity = 43
        address = "987 Fake Street"
        merchantName = "Bob's Pizza"
        parseAndSave([name, description, price, quantity, address, merchantName])
        parseAndSave([name, description, price, quantity, address, merchantName])
        
        # This will throw an exception if the models haven't been persisted properly,
        # or if they have been persisted multiple times
        customer = Customer.objects.get(name=name)
        item = Item.objects.get(description=description, price=price)
        merchant = Merchant.objects.get(address=address, name=merchantName)
        Transaction.objects.get(customer=customer, item=item, merchant=merchant, quantity=quantity)
    
    def test_parse_line_customer(self):
        name = "Fooo Bar"
        customer = parseAndSave([name, "$20 Sneakers for $5", "5.0", "1", "123 Fake St", "Sneaker Store Emporium"])[0]
        self.assertEqual(customer.name, name)

    def test_parse_line_item(self):
        description = "holy porkchops batman!"
        price = 32.1
        item = parseAndSave(["The Oatmeal", description, str(price), "13", "College Ave", "CTB"])[1]
        self.assertEqual(item.description, description)
        self.assertEqual(item.price, price)

    def test_parse_line_merchant(self):
        name = "Collegetown Bagles"
        address = "142 College Ave Ithaca NY"
        merchant = parseAndSave(["The Oatmeal", "yeahh", "4334.23", "13", address, name])[2]
        self.assertEqual(merchant.name, name)
        self.assertEqual(merchant.address, address)

    def test_parse_line_transaction(self):
        quantity = 808
        customer, item, merchant, transaction = parseAndSave(["The Oatmeal", "yeahh", "4334.23", str(quantity), "12 44th Street New York City", "Jamba Juice"])
        self.assertEqual(transaction.customer, customer)
        self.assertEqual(transaction.item, item)
        self.assertEqual(transaction.merchant, merchant)
        self.assertEqual(transaction.quantity, quantity)
        
    def test_get_revenue(self):
        prices = (23, 43, 808, 21)
        quantities = (1, 20, 43, 99)
        
        data = ("""Snake Plissken    $10 off $20 of food    %f    %%d    987 Fake St    Bob's Pizza
Amy Pond    $30 of awesome for $10    %f    %%d    456 Unreal Rd    Tom's Awesome Shop
Marty McFly    $20 Sneakers for $5    %f    %%d    123 Fake St    Sneaker Store Emporium
Snake Plissken    $20 Sneakers for $5    %f    %%d    123 Fake St    Sneaker Store Emporium""" % prices) % quantities 

        [parseAndSave(line.split("    ")) for line in data.splitlines()]
        
        revenue = sum((quantity * price for quantity, price in zip(quantities, prices)))
        
        self.assertEqual(revenue, getRevenue(Transaction.objects.all()))
    
    def test_get_revenue_sample_data(self):
        data = """Snake Plissken    $10 off $20 of food    10.0    2    987 Fake St    Bob's Pizza
Amy Pond    $30 of awesome for $10    10.0    5    456 Unreal Rd    Tom's Awesome Shop
Marty McFly    $20 Sneakers for $5    5.0    1    123 Fake St    Sneaker Store Emporium
Snake Plissken    $20 Sneakers for $5    5.0    4    123 Fake St    Sneaker Store Emporium"""

        [parseAndSave(line.split("    ")) for line in data.splitlines()]
        
        self.assertEqual(95, getRevenue(Transaction.objects.all()))
        
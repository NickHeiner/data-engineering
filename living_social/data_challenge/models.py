from django.db import models

# The max lengths on the CharFields are pretty much arbitrary - I put in reasonable guesses based on the data I was provided, and
# a desire to err on the safe side of not crashing on some unusually long input.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    
class Item(models.Model):
    description = models.CharField(max_length=120)
    price = models.FloatField()
    
class Merchant(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    
class Transaction(models.Model):
    customer = models.ForeignKey(Customer)
    item = models.ForeignKey(Item)
    merchant = models.ForeignKey(Merchant)
    quantity = models.IntegerField()
    
    # True if this transaction was stored in the most
    # recently uploaded file; false otherwise.
    fromMostRecentFile = models.BooleanField()

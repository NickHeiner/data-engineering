from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=60)
    
class Item(models.Model):
    description = models.CharField(max_length=100)
    price = models.FloatField()
    
class Merchant(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=120)
    
class Transaction(models.Model):
    customer = models.ForeignKey(Customer)
    item = models.ForeignKey(Item)
    merchant = models.ForeignKey(Merchant)
    quantity = models.IntegerField()

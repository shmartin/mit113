from django.db import models
from inventory.models import Inventory

# Create your models here.

class Order(models.Model):
    oorder = 1
    odate = 1
    oquantity = 1
    oprice = 1

class Transaction(models.Model):
    pass
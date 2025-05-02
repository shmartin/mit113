from django.db import models
from inventory.models import Inventory

# Create your models here.

class Sale(models.Model):
    sprice = models.IntegerField()
    sdate = models.DateField(auto_now_add=True)
    ssub_total = models.FloatField()
    sgrand_total = models.FloatField()
    stax_amount = models.FloatField()
    stax_percentage = models.FloatField()
    samount_payed = models.FloatField()
    samount_change = models.FloatField()

class Order(models.Model):
    tid = models.ForeignKey(Sale, on_delete=models.CASCADE)
    oorder = 1
    odate = 1
    oprice = 1
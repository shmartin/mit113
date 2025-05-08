from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product, Inventory, Extra

# Create your models here.

class Sale(models.Model):
    eid = models.ForeignKey(User, on_delete=models.CASCADE)
    sdate = models.DateTimeField(auto_now_add=True)
    stotal = models.FloatField(default=0)
    spayed = models.FloatField(default=0)
    schange = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} {self.sdate}'

class Order(models.Model):
    tid = models.ForeignKey(Sale, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    iid = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tid} {self.pid.pname}'

class SaleExtra(models.Model):
    tid = models.ForeignKey(Sale, on_delete=models.CASCADE)
    exid = models.ForeignKey(Extra, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tid} | {self.exid.exname} | {self.exid.exprice}'
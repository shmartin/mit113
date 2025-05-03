from django.db import models

# Create your models here.

class Product(models.Model):
    pname = models.CharField(max_length=64)
    pprice = models.FloatField()

    def __str__(self):
        return f'{self.pname}'

class Inventory(models.Model):
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    pquantity = models.IntegerField()
    pdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.pdate} | {self.pquantity}x {self.pid.pname} @ {self.pid.pprice}'

class Extra(models.Model):
    exname = models.CharField(max_length=64)
    exprice = models.FloatField()

    def __str__(self):
        return f'{self.exname}'
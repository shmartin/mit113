from django.db import models

# Create your models here.

class Product(models.Model):
    pname = models.CharField(max_length=64)
    pprice = models.IntegerField()

    def __str__(self):
        return f"{self.pname}"

class Inventory(models.Model):
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    pquantity = models.IntegerField()
    pdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pid.pname} | {self.pdate} | {self.pid.pprice} | {self.pquantity}"
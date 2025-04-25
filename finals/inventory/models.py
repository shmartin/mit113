from django.db import models

# Create your models here.

class Product(models.Model):
    pname = models.CharField(max_length=64)
    pquantity = models.IntegerField(null=True, blank=True)
    pdate = models.DateField(null=True, blank=True)
    pprice = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.pname} | {self.pdate} | {self.pprice} | {self.pquantity}"
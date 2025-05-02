from django.db import models
from inventory.models import Product

# Create your models here.

class Sale(models.Model):
    sdate = models.DateField(auto_now_add=True)
    ssub_total = models.FloatField(default=0)
    sgrand_total = models.FloatField(default=0)
    stax_amount = models.FloatField(default=0)
    stax_percentage = models.FloatField(default=0)
    samount_payed = models.FloatField(default=0)
    samount_change = models.FloatField(default=0)

    def __str__(self):
        return f'{self.id} {self.sdate}'

# order normalize
# order detail
class Order(models.Model):
    tid = models.ForeignKey(Sale, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    odate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.tid.sdate} {self.pid.pname}'

# order head
# date, time, reference
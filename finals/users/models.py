from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    POSITION_CASHIER = 'Cshr'
    POSITION_INVENTORY = 'Invt'

    POSITION_CHOICES = [
        (POSITION_CASHIER, 'Cashier'),
        (POSITION_INVENTORY, 'Inventory'),
    ]
    
    eid = models.ForeignKey(User, on_delete=models.CASCADE)
    epos = models.CharField(choices=POSITION_CHOICES, default=POSITION_INVENTORY, max_length=16)

    def __str__(self):
        return f'Username: {self.eid.username}, Access: {self.epos}'
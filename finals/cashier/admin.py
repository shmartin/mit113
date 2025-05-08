from django.contrib import admin
from .models import Sale, Order, SaleExtra

# Register your models here.

admin.site.register(Sale)
admin.site.register(Order)
admin.site.register(SaleExtra)
from django.contrib import admin
from .models import Product, Inventory, Extra

# Register your models here.

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Extra)
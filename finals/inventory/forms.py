from django import forms
from .models import Product, Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['pid', 'pquantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pname', 'pprice']
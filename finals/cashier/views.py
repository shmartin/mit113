from django.shortcuts import render
from django.db.models import Sum
from inventory.models import Product

# Create your views here.
def cashier(request):
    all_product = Product.objects.annotate(pquantity=Sum('inventory__pquantity'))
    context = {}
    context['product'] = all_product
    return render(request, 'cashier/cashier.html', context)
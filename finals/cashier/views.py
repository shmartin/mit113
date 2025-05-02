from django.shortcuts import render, redirect
from django.db.models import Sum
from inventory.models import Product

# Create your views here.
def cashier(request):
    all_product = Product.objects.annotate(pquantity=Sum('inventory__pquantity'))

    if request.method == 'POST':
        if 'add' in request.POST:
            return redirect('/cashier')

    context = {}
    context['product'] = all_product
    return render(request, 'cashier/cashier.html', context)
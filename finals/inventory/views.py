from django.shortcuts import render, redirect
from .models import Inventory
from .forms import InventoryForm

# Create your views here.
def inventory(request):
    form = InventoryForm()
    all_inventory = Inventory.objects.all().select_related('pid')

    if request.method == 'POST':
        if 'add' in request.POST:
            form = InventoryForm(request.POST)
            form.save()
            return redirect('/inventory')

    context = {}
    context['inventory'] = all_inventory
    context['form'] = form

    return render(request, 'inventory/inventory.html', context)
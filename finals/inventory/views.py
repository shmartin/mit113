from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory
from .forms import InventoryForm
import logging

# Create your views here.

@login_required
def inventory(request):
    form = InventoryForm()
    all_inventory = Inventory.objects.all().select_related('pid')
    logger = logging.getLogger('django')

    if request.method == 'POST':
        if 'add' in request.POST:
            pk = request.POST.get('add')
            if not pk:
                form = InventoryForm(request.POST)
            else:
                inv = Inventory.objects.get(id=pk)
                form = InventoryForm(request.POST, instance=inv)
            form.save()
            form = InventoryForm()
            return redirect('/inventory/')

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            inv = Inventory.objects.get(id=pk)
            inv.delete()
            return redirect('/inventory/')

        elif 'update' in request.POST:
            pk = request.POST.get('update')
            inv = Inventory.objects.get(id=pk)
            form = InventoryForm(instance=inv)


    context = {}
    context['inventory'] = all_inventory
    context['form'] = form

    return render(request, 'inventory/inventory.html', context)
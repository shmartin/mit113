from django.shortcuts import render

# Create your views here.
def inventory_render(request):
    return render(request, 'inventory/inventory.html')
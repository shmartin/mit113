from django.shortcuts import render

# Create your views here.
def cashier_render(request):
    return render(request, 'cashier/cashier_render.html')
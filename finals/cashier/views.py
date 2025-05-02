from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from inventory.models import Product
from django.contrib.auth.decorators import login_required
from .models import Sale, Order

# Create your views here.

@login_required
def cashier(request):
    all_product = Product.objects.annotate(pquantity=Sum('inventory__pquantity'))

    newsale = None
    newsale_orders = Order.objects.none()
    total_price = 0

    newsale_id = request.session.get('current_sale_id')

    if newsale_id:
        try:
            newsale = Sale.objects.get(pk=newsale_id)
            newsale_orders = Order.objects.filter(tid=newsale).select_related('pid')
            aggregate_result = newsale_orders.annotate(item_price=F('pid__pprice')).aggregate(total_price=Sum('item_price'))
            total_price = aggregate_result['total_price'] if aggregate_result['total_price'] is not None else 0
        except Sale.DoesNotExist:
            del request.session['current_sale_id']
            newsale = None
            newsale_orders = Order.objects.none()
            total_price = 0

    if request.method == 'POST':
        if 'newsale' in request.POST:
            sale = Sale.objects.create()
            request.session['current_sale_id'] = sale.pk
            return redirect('/cashier')

        elif 'add' in request.POST:
            pk = request.POST.get('add')
            if newsale:
                try:
                    pname = get_object_or_404(Product, pk=pk)
                    order = Order.objects.create(pid=pname,tid=newsale)
                except Product.DoesNotExist:
                    print(f'Error: {pk} not found')
                except Exception as e:
                    print(f'{e}')
            else:
                print('No Current Sale')

            return redirect('/cashier')

        elif 'remove' in request.POST:
            pk = request.POST.get('remove')
            order = get_object_or_404(Order, id=pk)
            order.delete()

    context = {}
    context['product'] = all_product
    context['orders'] = newsale_orders
    context['total'] = total_price
    return render(request, 'cashier/cashier.html', context)
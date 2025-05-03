from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Order
from inventory.models import Product, Inventory

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

        elif 'add' in request.POST:
            pk = request.POST.get('add')
            if newsale:
                try:
                    with transaction.atomic():
                        pname = get_object_or_404(Product, pk=pk)
                        order_quantity = 1
                        remaining = order_quantity
                        inv = Inventory.objects.filter(pid=pk).order_by('pdate')
                        total_inv = inv.aggregate(total=Sum('pquantity'))['total'] or 0
                        if total_inv >= order_quantity:
                            for item in inv:
                                if remaining > 0:
                                    if item.pquantity >= remaining:
                                        item.pquantity -= remaining
                                        item.save()
                                        remaining = 0
                                    else:
                                        remaining -= item.pquantity
                                        item.pquantity = 0
                                        item.save()
                            order = Order.objects.create(pid=pname,tid=newsale)
                        elif total_inv > 0:
                            pass
                        else:
                            pass
                except Product.DoesNotExist:
                    messages.error(request, f'Product not found: {pk}')
                except Exception as e:
                    messages.error(request, f'Error processing order: {e}')
            else:
                print('No Current Sale')

        elif 'remove' in request.POST:
            pk = request.POST.get('remove')
            try:
                with transaction.atomic():
                    delete_order = Order.objects.get(id=pk)
                    linked_products = delete_order.pid
                    inventory_update = Inventory.objects.filter(pid=linked_products).order_by('-pdate').first()
                    if inventory_update:
                        inventory_update.pquantity += 1
                        inventory_update.save()
                    else:
                        pass
                    delete_order.delete()
                messages.success(request, 'Item removed successfully.')
            except Order.DoesNotExist:
                messages.error(request, 'Item already removed or not found.')
            except Exception as e:
                messages.error(request, f'Error removing order: {e}')

        elif 'complete' in request.POST:
            pk = request.POST.get('complete')

        return redirect('/cashier')

    context = {}
    context['product'] = all_product
    context['orders'] = newsale_orders
    context['total'] = total_price
    return render(request, 'cashier/cashier.html', context)
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Order
from inventory.models import Product, Inventory, Extra

# Create your views here.

@login_required
def cashier(request):
    all_product = Product.objects.annotate(pquantity=Sum('inventory__pquantity'))
    extras = Extra.objects.all()

    newsale = None
    newsale_orders = Order.objects.none()
    total_price = 0

    newsale_id = request.session.get('newsale_id')

    if newsale_id:
        try:
            newsale = Sale.objects.get(pk=newsale_id)
            newsale_orders = Order.objects.filter(tid=newsale).select_related('pid', 'iid')
            aggregate_result = newsale_orders.annotate(item_price=F('pid__pprice')).aggregate(total_price=Sum('item_price'))
            total_price = aggregate_result['total_price'] if aggregate_result['total_price'] is not None else 0
        except Sale.DoesNotExist:
            del request.session['newsale_id']
            newsale = None
            newsale_orders = Order.objects.none()
            total_price = 0

    if not newsale and request.method == 'GET':
        if request.user.is_authenticated:
            newsale = Sale.objects.create(eid=request.user)
            request.session['newsale_id'] = newsale.pk
        else:
            return redirect('/')

    if request.method == 'POST':
        if 'add' in request.POST:
            pk = request.POST.get('add')
            if newsale:
                try:
                    with transaction.atomic():
                        pname = get_object_or_404(Product, pk=pk)
                        order_quantity = 1
                        inv = Inventory.objects.filter(pid=pk, pquantity__gt=0).order_by('pdate').first()
                        if inv:
                            inv.pquantity -= 1
                            inv.save()
                            order = Order.objects.create(pid=pname, tid=newsale, iid=inv)
                            newsale.stotal = Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0
                            newsale.save()
                        else:
                            pass
                except Product.DoesNotExist:
                    messages.error(request, f'Product not found: {pk}')
                except Exception as e:
                    messages.error(request, f'Error processing order: {e}')
            else:
                messages.error(request, 'Start new sale first.')

        elif 'remove' in request.POST:
            pk = request.POST.get('remove')
            try:
                with transaction.atomic():
                    delete_order = Order.objects.get(id=pk)
                    inventory_update = delete_order.iid
                    if inventory_update:
                        inventory_update.pquantity += 1
                        inventory_update.save()
                    else:
                        pass
                    delete_order.delete()
                    if newsale:
                        newsale.stotal = Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0
                        newsale.save()
                    messages.success(request, 'Item removed successfully.')
            except Order.DoesNotExist:
                messages.error(request, 'Item already removed or not found.')
            except Exception as e:
                messages.error(request, f'Error removing order: {e}')

        elif 'complete_sale' in request.POST and newsale:
            pk = request.POST.get('complete_sale')

        return redirect('/cashier')

    context = {}
    context['product'] = all_product
    context['orders'] = newsale_orders
    context['total'] = total_price
    context['extras'] = extras
    context['change'] = total_price
    return render(request, 'cashier/cashier.html', context)
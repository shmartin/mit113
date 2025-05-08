from datetime import date
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Sale, Order, SaleExtra
from inventory.models import Product, Inventory, Extra
from users.models import Employee

def is_cashier(user):
    if user.is_authenticated:
        try:
            employee = Employee.objects.get(eid=user)
            return employee.epos == Employee.POSITION_CASHIER
        except Employee.DoesNotExist:
            return False
    return False

# Create your views here.

@login_required
@user_passes_test(is_cashier, login_url='/')
def cashier(request):
    all_product = Product.objects.annotate(pquantity=Sum('inventory__pquantity'))
    extras = Extra.objects.all()

    newsale = None
    newsale_orders = Order.objects.none()
    sale_extra = SaleExtra.objects.none()
    extra_total_price = 0
    total_price = 0

    newsale_id = request.session.get('newsale_id')

    if newsale_id:
        try:
            newsale = Sale.objects.get(pk=newsale_id)
            newsale_orders = Order.objects.filter(tid=newsale).select_related('pid', 'iid')
            sale_extra = SaleExtra.objects.filter(tid=newsale).select_related('exid')
            aggregate_result = newsale_orders.annotate(item_price=F('pid__pprice')).aggregate(total_price=Sum('item_price'))
            total_price = aggregate_result['total_price'] if aggregate_result['total_price'] is not None else 0
            aggregate_extra = sale_extra.aggregate(total_price=Sum('exid__exprice'))
            extra_total_price = aggregate_extra['total_price'] if aggregate_extra['total_price'] is not None else 0
        except Sale.DoesNotExist:
            del request.session['newsale_id']
            newsale = None
            newsale_orders = Order.objects.none()
            sale_extra = SaleExtra.objects.none()
            extra_total_price = 0
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
                            newsale.stotal = (Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0) + (SaleExtra.objects.filter(tid=newsale).aggregate(total=Sum('exid__exprice'))['total'] or 0)
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
                        newsale.stotal = (Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0) + (SaleExtra.objects.filter(tid=newsale).aggregate(total=Sum('exid__exprice'))['total'] or 0)
                        newsale.save()
                    messages.success(request, 'Item removed successfully.')
            except Order.DoesNotExist:
                messages.error(request, 'Item already removed or not found.')
            except Exception as e:
                messages.error(request, f'Error removing order: {e}')

        elif 'add_extra' in request.POST:
            if newsale:
                pk = request.POST.get('add_extra')
                try:
                    with transaction.atomic():
                        exname = get_object_or_404(Extra, pk=pk)
                        sale_extra = SaleExtra.objects.create(tid=newsale, exid=exname)
                        newsale.stotal = (Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0) + (SaleExtra.objects.filter(tid=newsale).aggregate(total=Sum('exid__exprice'))['total'] or 0)
                        newsale.save()

                except Extra.DoesNotExist:
                    messages.error(request, f'Error: Extra {newsale.id} not found')
                except Exception as e:
                    messages.error(request, f'Error processing extra order: {e}')

        elif 'remove_extra' in request.POST:
            pk = request.POST.get('remove_extra')
            if newsale:
                try:
                    with transaction.atomic():
                        delete_extra = SaleExtra.objects.get(id=pk)

                        if delete_extra.tid == newsale:
                            delete_extra.delete()
                            newsale.stotal = (Order.objects.filter(tid=newsale).annotate(item_price=F('pid__pprice')).aggregate(total=Sum('item_price'))['total'] or 0) + (SaleExtra.objects.filter(tid=newsale).aggregate(total=Sum('exid__exprice'))['total'] or 0)
                            newsale.save()

                except SaleExtra.DoesNotExist:
                    messages.error(request, 'SaleExtra not found')
                except Exception as e:
                    messages.error(request, f'Error removing extra item: {e}')


        elif 'complete_sale' in request.POST and newsale:
            amount_tendered_str = request.POST.get('amount_tendered')
            try:
                amount_tendered = Decimal(amount_tendered_str)
                grand_total = Decimal(newsale.stotal)

                if amount_tendered >= grand_total:
                    change = amount_tendered - grand_total

                    with transaction.atomic():
                        newsale.spayed = float(amount_tendered)
                        newsale.schange = float(change)
                        newsale.is_completed = True
                        newsale.save()

                        empty_inventories = Inventory.objects.filter(pquantity__lte=0)
                        deleted_count, _ = empty_inventories.delete()

                        del request.session['newsale_id']
                else:
                    messages.error(request, f'Tendered insufficient')

            except InvalidOperation:
                messages.error(request, 'Invalid amount tendered')
            except Exception as e:
                messages.error(request, f'Error completing sale: {e}')

        return redirect('/cashier')

    context = {}
    context['product'] = all_product
    context['orders'] = newsale_orders
    context['saleextra'] = sale_extra
    context['grandtotal'] = total_price + extra_total_price
    context['extras'] = extras
    context['change'] = total_price
    return render(request, 'cashier/cashier.html', context)
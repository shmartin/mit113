from datetime import datetime, date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Q
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import TruncDate
from django.db.models import Value
from cashier.models import Order, Sale, SaleExtra
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
def reports(request):
    completed_sales_queryset = Sale.objects.filter(is_completed=True)
    total_product_orders_queryset = Order.objects.all()
    total_extra_orders_queryset = SaleExtra.objects.all()

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = None
    end_date = None

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            start_datetime = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())
            completed_sales_queryset = completed_sales_queryset.filter(sdate__gte=start_datetime)
            total_product_orders_queryset = total_product_orders_queryset.filter(tid__sdate__gte=start_datetime)
            total_extra_orders_queryset = total_extra_orders_queryset.filter(tid__sdate__gte=start_datetime)
        except ValueError:
            messages.error(request, "Invalid start date format.")

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            end_datetime = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())
            completed_sales_queryset = completed_sales_queryset.filter(sdate__lte=end_datetime)
            total_product_orders_queryset = total_product_orders_queryset.filter(tid__sdate__lte=end_datetime)
            total_extra_orders_queryset = total_extra_orders_queryset.filter(tid__sdate__lte=end_datetime)
        except ValueError:
            messages.error(request, "Invalid end date format.")


    completed_sales = completed_sales_queryset.order_by('-sdate')

    total_revenue_aggregation = completed_sales.aggregate(total_sum=Sum('stotal'))
    total_revenue = total_revenue_aggregation['total_sum'] if total_revenue_aggregation['total_sum'] is not None else Decimal(0)


    inventory_summary = Product.objects.annotate(total_remaining_quantity=Sum('inventory__pquantity')).order_by('pname')


    total_product_orders = total_product_orders_queryset.values('pid__pname').annotate(total_ordered_quantity=Sum(Value(1))).order_by('pid__pname')

    total_extra_orders = total_extra_orders_queryset.values('exid__exname').annotate(total_ordered_quantity=Sum(Value(1))).order_by('exid__exname')

    context = {}
    context['completed_sales'] = completed_sales
    context['total_revenue'] = total_revenue
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['inventory_summary'] = inventory_summary
    context['total_product_orders'] = total_product_orders
    context['total_extra_orders'] = total_extra_orders

    return render(request, 'reports/reports.html', context)
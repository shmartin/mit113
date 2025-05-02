from django.urls import path
from . import views

urlpatterns = [
    path('cashier/',views.cashier),
]
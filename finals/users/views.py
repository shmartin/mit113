from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Employee

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            user_type = Employee.epos
            if user_type == 'inventory':
                return redirect('/inventory')
            elif user_type == 'Cashier':
                return redirect('/cashier')
    else:
        form = AuthenticationForm()

    context = {}
    context['form'] = form

    return render(request, 'users/login.html', context)

def logout(request):
    if request.method == 'POST':
        return redirect('login')
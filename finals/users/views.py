from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Employee

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            try:
                employee = Employee.objects.get(eid=user)
                user_position = employee.epos

                if user_position == Employee.POSITION_INVENTORY:
                    return redirect('inventory/')
                elif user_position == Employee.POSITION_CASHIER:
                    return redirect('cashier/')
                else:
                    messages.warning(request, "Your account has an unrecognized position.")
                    auth_logout(request)
                    return redirect('/')

            except Employee.DoesNotExist:
                messages.error(request, "User account is not linked to an employee profile.")
                auth_logout(request)
                return redirect('/')

        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'users/login.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')
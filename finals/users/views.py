from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
#from users.forms import EmployeeForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('inventory:inventory')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
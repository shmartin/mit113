from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Employee

# Create your views here.

def login(request):
    """
    Handles user login using Django's AuthenticationForm.
    Redirects based on Employee position upon successful login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) # Log the user in

            # --- Redirection Logic based on Employee Position ---
            try:
                # Attempt to get the Employee object linked to the logged-in user
                employee = Employee.objects.get(eid=user)
                user_position = employee.epos # Get the position from the specific Employee object

                if user_position == Employee.POSITION_INVENTORY: # Use constants for comparison
                    # Redirect to inventory page
                    return redirect('inventory/') # Use URL name if defined
                elif user_position == Employee.POSITION_CASHIER: # Use constants for comparison
                    # Redirect to cashier page
                    return redirect('cashier/') # Use URL name if defined
                else:
                    # Handle cases with unexpected positions (optional)
                    messages.warning(request, "Your account has an unrecognized position.")
                    auth_logout(request) # Log out users with unrecognized positions
                    return redirect('/')

            except Employee.DoesNotExist:
                # Handle users who are not linked to an Employee object
                messages.error(request, "User account is not linked to an employee profile.")
                auth_logout(request) # Log out users without an employee profile
                return redirect('/')
            # --- End Redirection Logic ---

        else:
            # Form is not valid (e.g., wrong username/password)
            # AuthenticationForm automatically adds errors to the form
            messages.error(request, "Invalid username or password.") # Add a general error message

    else: # GET request
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'users/login.html', context)


def logout(request):
    """
    Logs the user out and redirects to the login page.
    """
    # Use Django's built-in logout function
    auth_logout(request)
    messages.success(request, "You have been logged out.") # Optional success message
    # Redirect to the login page (using URL name is recommended)
    return redirect('/')
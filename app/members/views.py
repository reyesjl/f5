from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import CustomLoginForm, CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from core.decorators import is_admin

@login_required
def dashboard(request):
    if request.user.is_staff:
        return render(request, "members/dashboard.html")
    else:
        return render(request, "members/user_dashboard.html")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('dashboard')  # Redirect to user dashboard or another page
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)

@login_required
def logmeout(request):
    logout(request)
    return redirect('login')

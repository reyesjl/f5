from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import MemberCreationForm, MemberAuthenticationForm
from .models import CustomUser

def member_signup(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('member-dashboard', username=user.username)
    else:
        form = MemberCreationForm()
    return render(request, 'members/signup.html', {'form': form})

def member_login(request):
    if request.method == 'POST':
        form = MemberAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('member-dashboard', username=user.username)
    else:
        form = MemberAuthenticationForm()
    return render(request, 'members/login.html', {'form': form})

@login_required
def member_dashboard(request, username):
    user = CustomUser.objects.get(username=username)
    
    if user.is_superuser:
        return redirect('admin-dashboard', username=user.username)
    elif user.groups.filter(name='trainer').exists():
        return redirect('trainer-dashboard', username=user.username)
    elif user.groups.filter(name='player').exists():
        return redirect('player-dashboard', username=user.username)
    else:
        # Default dashboard view for users without specific groups
        return render(request, 'members/dashboard.html', {'user': user})
    
@login_required
def admin_dashboard(request, username):
    user = CustomUser.objects.get(username=username)
    messages.info(request, "Camp registration is up 5% today.", extra_tags="info")
    messages.info(request, "Asau has released a new plan.", extra_tags="info")
    context = {
        'user': user,
    }
    return render(request, 'members/admin_dashboard.html', context)

@login_required
def trainer_dashboard(request, username):
    user = CustomUser.objects.get(username=username)
    context = {
        'user': user,
    }
    return render(request, 'members/trainer_dashboard.html', context)

@login_required
def player_dashboard(request, username):
    user = CustomUser.objects.get(username=username)
    messages.success(request, "You have earned 10xp for logging in today.", extra_tags="success")
    context = {
        'user': user,
    }
    return render(request, 'members/player_dashboard.html', context)
    
def member_logout(request):
    logout(request)
    return redirect('member-login')

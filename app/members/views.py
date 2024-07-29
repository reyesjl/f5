from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from core.decorator import user_has_role, is_trainer, is_staff, is_staff_or_trainer
from core.utils import check_user, get_object_or_error
from django.contrib.auth.decorators import login_required
from .forms import MemberCreationForm, MemberUpdateForm, MemberAuthenticationForm, SupportTicketForm, UpdateProfileForm, UpdateAvatarForm
from .models import CustomUser, UserProfile
from events.models import Event
from blog.models import Article
from health.models import Plan, Client, TrainerSessionRequest

@login_required
@user_has_role("health_manager")
def member_list(request):
    users = CustomUser.objects.all()

    # Filter by search query
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query)

    # Filter by user group
    user_group_filter = request.GET.get('user_group', 'all')
    if user_group_filter != 'all':
            users = users.filter(groups__name=user_group_filter)
            
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, "members/member-list.html", context)

@is_staff_or_trainer
def member_detail(request, username):
    user = get_object_or_error(request,CustomUser, username=username)
    context = {
        'profile': user,
    }
    return render(request, "members/member-detail.html", context)

@is_staff_or_trainer
def member_update(request, username):
    profile = get_object_or_error(request,CustomUser, username=username)
    print(profile)

    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, "User has been updated.", extra_tags="info")
            return redirect('member-list')
    else:
        form = MemberUpdateForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, "members/member_update.html", context)

def member_signup(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('member-login')
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
                return redirect('member-dashboard')
    else:
        form = MemberAuthenticationForm()
    return render(request, 'members/login.html', {'form': form})

def member_login_support(request):
    return render(request, 'members/login_support.html')

def member_support_form(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            support_ticket = form.save(commit=False)
            support_ticket.user = request.user
            support_ticket.save()
            return redirect('member-support-success')
    else:
        form = SupportTicketForm()
    return render(request, 'members/support/support_form.html', {'form': form})

def member_support_success(request):
    return render(request, 'members/support/support_success.html')

def member_profile(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        messages.error(request, "User not found", extra_tags="error")
        return render(request, "core/error.html", {"message": message})
    
    has_trainer = check_user(request.user, "trainer")
    if (has_trainer):
        clients = Client.objects.by_user(request.user)
        
    context = {
        'profile': user,
        'has_trainer': has_trainer,
    }
    return render(request, 'members/profile.html', context)

@login_required
def member_dashboard(request):
    user = request.user
    profile = get_object_or_error(request, UserProfile, user=user)

    if user.is_staff:
        context = {
            user: 'user',
            profile: 'profile',
        }
        messages.info(request, "Thank you for being a valued staff member. +10px", extra_tags="info")
        return render(request, 'members/staff_dashboard.html', context)
    elif user.is_trainer:
        requests = TrainerSessionRequest.objects.filter(trainer=user)
        context = {
            'user': user,
            'requests': requests,
        }
        messages.info(request, "Thank you for being a valued trainer. +10px", extra_tags="info")
        return render(request, 'members/trainer_dashboard.html', context)
    else:
        requests = TrainerSessionRequest.objects.filter(user=user)
        messages.info(request, "Welcome back, and thank you for using the platform!", extra_tags="info")
        context = {
            'user': user,
            'requests': requests,
        }
        return render(request, 'members/dashboard.html', context)

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('member-dashboard')
    else:
        form = UpdateProfileForm(instance=user)
    
    context = {
        'form': form,
    }
    return render(request, "members/settings/update_profile_form.html", context)

@login_required
def update_avatar(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateAvatarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('member-dashboard')
    else:
        form = UpdateAvatarForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, "members/settings/update_avatar_form.html", context)
    
def member_logout(request):
    logout(request)
    request.session.flush()
    return redirect('member-login')

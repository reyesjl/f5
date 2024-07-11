from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from core.decorator import user_has_role
from core.utils import check_user
from django.contrib.auth.decorators import login_required
from .forms import MemberCreationForm, MemberAuthenticationForm
from .models import CustomUser, UserProfile, PlayerProfile, HealthProfile
from events.models import Event
from blog.models import Article
from health.models import Plan, Client

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
                request.session['username'] = username
                return redirect('member-dashboard', username=user.username)
    else:
        form = MemberAuthenticationForm()
    return render(request, 'members/login.html', {'form': form})

def member_login_support(request):
    return render(request, 'members/login_support.html')

def member_profile(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        messages.error(request, "User not found", extra_tags="error")
        return render(request, "core/error.html", {"message": message})
    
    # Fetch user profiles
    player_profile = PlayerProfile.objects.filter(user=user).first()
    health_profile = HealthProfile.objects.filter(user=user).first()
    
    has_trainer = check_user(request.user, "trainer")
    if (has_trainer):
        clients = Client.objects.by_user(request.user)
        
    context = {
        'profile': user,
        'player_profile': player_profile,
        'health_profile': health_profile,
        'has_trainer': has_trainer,
    }
    return render(request, 'members/profile.html', context)

@login_required
def member_dashboard(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
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
@user_has_role("admin")
def admin_dashboard(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    total_users = CustomUser.objects.count()
    total_events = Event.objects.count()
    total_articles = Article.objects.count()

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'total_articles': total_articles,
        'user': user,
    }
    return render(request, 'members/admin_dashboard.html', context)

@login_required
@user_has_role("trainer")
def trainer_dashboard(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    health_clients = Client.objects.by_trainer(username).count()
    context = {
        'user': user,
        'health_clients': health_clients,
    }
    return render(request, 'members/trainer_dashboard.html', context)

@login_required
@user_has_role("player")
def player_dashboard(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    player_profile = PlayerProfile.objects.filter(user=user).first()
    health_profile = HealthProfile.objects.filter(user=user).first()
    
    context = {
        'user': user,
        'player_profile': player_profile,
        'health_profile': health_profile,
    }
    return render(request, 'members/player_dashboard.html', context)
    
def member_logout(request):
    logout(request)
    request.session.flush()
    return redirect('member-login')

from django.shortcuts import redirect, render
from django.contrib import messages

from core.decorator import user_has_role
from .models import Plan, Client
from blog.models import Article
from .forms import PlanForm
from members.models import CustomUser, HealthProfile, PlayerProfile
from core.utils import check_user


def index(request):
    plans = Plan.objects.published().featured()
    can_manage = check_user(request.user, "health_manager")

    context = {
        "plans": plans,
        "can_manage": can_manage
    }
    return render(request, "health/index.html", context)

def strength_index(request):
    plans = Plan.objects.published().by_type("strength_and_conditioning")
    articles = Article.objects.published().by_type("strength_and_conditioning")
    can_manage = check_user(request.user, "health_manager")

    context = {
        "plans": plans,
        "articles": articles,
        "can_manage": can_manage,
    }
    return render(request, "health/strength.html", context)

def nutrition_index(request):
    plans = Plan.objects.published().by_type("nutrition")
    articles = Article.objects.published().by_type("nutrition")
    can_manage = check_user(request.user, "health_manager")

    context = {
        "plans": plans,
        "articles": articles,
        "can_manage": can_manage,
    }
    return render(request, "health/nutrition.html", context)

def mental_index(request):
    plans = Plan.objects.published().by_type("mental")
    articles = Article.objects.published().by_type("mental")
    can_manage = check_user(request.user, "health_manager")

    context = {
        "plans": plans,
        "articles": articles,
        "can_manage": can_manage,
    }
    return render(request, "health/mental.html", context)

@user_has_role("health_manager")
def plan_list(request):
    plans = Plan.objects.all()
    can_manage = check_user(request.user, "health_manager")

    # Filter on visibility (manager only!)
    # e.g. ('draft' or 'published')
    visibility = request.GET.get("visibility")
    if visibility and can_manage:
        plans = Plan.objects.all()
        plans = plans.by_visibility(visibility)

    # Filter on status
    status = request.GET.get("plan_status")
    if status == "featured":
        plans = plans.featured()

    # Filter on type
    type = request.GET.get("plan_type")
    if type:
        if type != 'all':
            plans = plans.by_type(type)

    context = {
        "plans": plans,
        "can_manage": can_manage,
    }
    return render(request, "plans/plan_list.html", context)

@user_has_role("health_manager")
def plan_create(request):
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('health-home')
    else:
        form = PlanForm()

    return render(request, "plans/plan_create.html", {"form": form})

def plan_detail(request, slug):
    can_manage = check_user(request.user, "health_manager")
    try:
        plan = Plan.objects.by_slug(slug=slug)
    except Plan.DoesNotExist:
        messages.error(request, "The requested plan does not exist.", extra_tags="error")
        return render(request, "core/error.html")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}", extra_tags="error")
        return render(request, "core/error.html")
    
    if not can_manage and plan.status == 'draft':
        messages.error(request, f"This plan is not published.", extra_tags="error")
        return render(request, "core/error.html")
    
    context = {
        "plan": plan,
        "can_manage": can_manage
    }
    
    return render(request, "plans/plan_detail.html", context)

@user_has_role("health_manager")
def plan_update(request, slug):
    try:
        plan_instance = Plan.objects.by_slug(slug=slug)
    except Plan.DoesNotExist:
        messages.error(request, "The requested plan does not exist.", extra_tags="error")
        return render(request, "core/error.html")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}", extra_tags="error")
        return render(request, "core/error.html")
    
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES, instance=plan_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Plan updated successfully.", extra_tags="success")
            return redirect('plan-list')
    else:
        form = PlanForm(instance=plan_instance)

    return render(request, "plans/plan_update.html", {"form": form})

@user_has_role("health_manager")
def plan_delete(request, slug):
    """
    Handles the deletion of an existing event.

    Parameters:
    - request: HTTP request object
    - slug: Slug of the plan to delete

    Returns:
    - Rendered HTML template for plan deletion confirmation
    - Redirects to health home on successful deletion
    """
    try:
        plan = Plan.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    if request.method == "POST":
        plan.delete()
        return redirect("health-home")
    
    return render(request, "plans/plan_delete_confirm.html", {"plan": plan})

@user_has_role("health_manager")
def quick_action(request, slug, action):
    try:
        plan = Plan.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    if action == 'toggle-featured':
        plan.featured = not plan.featured
    elif action == 'toggle-status':
        plan.status = 'published' if plan.status == 'draft' else 'draft'

    plan.save()
    return redirect('plan-list')

# clients
@user_has_role("trainer")
def client_list(request, trainer_username):
    clients = Client.objects.by_trainer(trainer_username)

    # Filter by search query
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(user__username__icontains=search_query)

    # Filter by user group
    user_group_filter = request.GET.get('user_group', 'all')
    if user_group_filter != 'all':
            clients = clients.filter(user__groups__name=user_group_filter)
    
    context = {
        'clients': clients,
    }
    return render(request, 'clients/client_list.html', context)

@user_has_role("trainer")
def client_add(request, trainer_username, client_username):
    # Fetch the trainer
    try:
        trainer = CustomUser.objects.get(username=trainer_username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {'message': message})
    
    # Fetch the user
    try:
        client = CustomUser.objects.get(username=client_username)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {'message': message})
    
    # Check Clients for instance
    if Client.objects.filter(user=client).exists():
        messages.info(request, "User is already a client.", extra_tags="info")
    else:
        Client.objects.create(user=client, trainer=trainer)
        messages.info(request, "User has been added.", extra_tags="info")

    player_profile, created_pp = PlayerProfile.objects.get_or_create(user=client, defaults={
        'position': '',
        'club': '',
        'tries_scored': 0,
        'tackles_made': 0,
        'minutes_played': 0,
    })
    
    health_profile, created_hp = HealthProfile.objects.get_or_create(user=client, defaults={
        'height': 0.00,
        'weight': 0.00,
    })

    if created_pp and created_hp:
        messages.success(request, 'Player and Health profiles have been initialized.', extra_tags="success")
    elif created_pp:
        messages.success(request, 'Player profile has been initialized.', extra_tags="success")
    elif created_hp:
        messages.success(request, 'Health profile has been initialized.', extra_tags="success")
    else:
        messages.info(request, 'Profiles already exist.', extra_tags="info")
    
    return redirect('client-list', trainer_username=trainer_username)

@user_has_role("trainer")
def client_remove(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {'message': message})
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client has been removed.", extra_tags="success")
        return redirect('client-list', request.user.username)
    
    return render(request, 'clients/client_remove_confirm.html', {'client': client})

@user_has_role("trainer")
def client_initialize(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {'message': message})
    
    player_profile, created_pp = PlayerProfile.objects.get_or_create(user=client.user, defaults={
        'position': '',
        'club': '',
        'tries_scored': 0,
        'tackles_made': 0,
        'minutes_played': 0,
    })
    
    health_profile, created_hp = HealthProfile.objects.get_or_create(user=client.user, defaults={
        'height': 0.00,
        'weight': 0.00,
    })

    if created_pp and created_hp:
        messages.success(request, 'Player and Health profiles have been initialized.', extra_tags="success")
    elif created_pp:
        messages.success(request, 'Player profile has been initialized.', extra_tags="success")
    elif created_hp:
        messages.success(request, 'Health profile has been initialized.', extra_tags="success")
    else:
        messages.info(request, 'Profiles already exist.', extra_tags="info")

    return redirect('client-list', request.user.username)

@user_has_role("trainer")
def client_detail(request, client_id):
    # fetch user object from client
    # fetch user profiles to display
    # show quick actions (remove client, reset info, etc)
    pass
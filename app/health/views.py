from django.shortcuts import redirect, render
from django.contrib import messages

from core.decorator import user_has_role, is_staff, is_trainer, is_staff_or_trainer
from .models import HealthProfile, Plan, Client
from blog.models import Article
from .forms import PlanForm, HealthProfileForm
from members.models import CustomUser
from core.utils import check_user, get_object_or_error

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

    # filter on event type
    plan_type = request.GET.get("type")
    if plan_type and plan_type != 'all':
        plans = plans.by_type(plan_type)

    context = {
        "type": plan_type,
        "plans": plans,
        "can_manage": can_manage,
    }
    return render(request, "plans/plan_list.html", context)

@is_staff_or_trainer
def plan_create(request):
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.author = request.user.username
            plan.save()
            return redirect('health-home')
    else:
        form = PlanForm()

    return render(request, "plans/plan_form.html", {"form": form})

def plan_detail(request, slug):
    plan = get_object_or_error(Plan, slug=slug)
    
    context = {
        "plan": plan,
    }
    
    return render(request, "plans/plan_detail.html", context)

@is_staff_or_trainer
def plan_update(request, slug):
    plan = get_object_or_error(Plan, slug=slug)
    
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.author = request.user.username
            plan.save()
            messages.success(request, "Plan updated successfully.", extra_tags="success")
            return redirect('plan-list')
    else:
        form = PlanForm(instance=plan)

    return render(request, "plans/plan_form.html", {"form": form})

@is_staff_or_trainer
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

# clients
@is_trainer
def client_list(request):
    trainer = get_object_or_error(CustomUser, username=request.user.username)
    clients = trainer.clients.all()

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

@is_trainer
def client_detail(request, client_id):
    client = get_object_or_error(Client, id=client_id)
    health_profile = get_object_or_error(HealthProfile, user=client.user)
    
    context = {
        'client': client,
        'health_profile': health_profile,
    }
    return render(request, 'clients/client_detail.html', context)

@is_trainer
def client_add(request, trainer_username, client_username):
    trainer = get_object_or_error(CustomUser, username=trainer_username)
    client = get_object_or_error(CustomUser, username=client_username)
    
    # Check if client already exists for this trainer
    if trainer.clients.filter(user=client).exists():
        messages.info(request, "User is already a client.", extra_tags="info")
    else:
        # Create Client object if it doesn't exist
        Client.objects.create(user=client, trainer=trainer)
        messages.info(request, "User has been added as a client.", extra_tags="info")
    
    return redirect('client-list')

@is_trainer
def client_remove(request, client_username):
    user = get_object_or_error(CustomUser, username=client_username) 
    client = get_object_or_error(Client, user=user)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client has been removed.", extra_tags="success")
        return redirect('client-list')
    
    return render(request, 'clients/client_remove_confirm.html', {'client': client})
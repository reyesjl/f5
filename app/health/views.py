from django.shortcuts import redirect, render
from django.contrib import messages

from core.decorator import user_has_role
from .models import Plan
from blog.models import Article
from .forms import PlanForm
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

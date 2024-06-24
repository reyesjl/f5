from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import Event, EventRole, Rsvp
from .forms import EventForm, EventRoleForm, RsvpForm, UpdateRsvpForm
from core.decorator import user_has_role
from core.utils import check_user


# Event Views
# =============================================================================

def event_list(request):
    # get all events
    events = Event.objects.all()

    # filter on event type
    event_type = request.GET.get("event_type")
    if event_type:
        events = events.filter_by_event_type(event_type)

    # filter on event status    
    event_status = request.GET.get("event_status")
    if event_status == "featured":
        events = events.featured()

    # only show upcoming events
    events = events.upcoming()
    can_manage = check_user(request.user, "event_manager")

    context = {
        "events": events,
        "can_manage": can_manage,
    }
    return render(request, "events/event_list.html", context)

def event_detail(request, slug):
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    can_manage = check_user(request.user, "event_manager")
    roles = event.roles.all()

    context = {
        "event": event, 
        "roles": roles,
        "can_manage": can_manage
    }
    return render(request, "events/event_detail.html", context)

@user_has_role("event_manager")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("event-list"))
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {"form": form})

@user_has_role("event_manager")
def event_update(request, slug):
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', slug=event.slug)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_update.html", {"form": form})

@user_has_role("event_manager")
def event_delete(request, slug):
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    if request.method == "POST":
        event.delete()
        return redirect("event-list")
    
    return render(request, "events/event_delete_confirm.html", {"event": event})

@user_has_role("event_manager")
def role_create(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Exception as e:
        message = e
        messages.errors(request, e, extra_tags="error")
        return render(request, "core/error.html", {"message": message})
    
    if request.method == "POST":
        form = EventRoleForm(request.POST)
        if form.is_valid():
            event_role = form.save(commit=False)
            event_role.event = event
            event_role.save()
            messages.success(request, "Role has been added.", extra_tags="success")
            return redirect('role-list', event_slug=event.slug)
    else:
        form = EventRoleForm()

    context = {
        "form": form,
        "event": event,
    }

    return render(request, "roles/role_create.html", context)


@user_has_role("event_manager")
def role_list(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    roles = event.roles.all()

    context = {
        "event": event, 
        "roles": roles,
    }

    return render(request, "roles/role_list.html", context)

@user_has_role("event_manager")
def role_delete(request, event_slug, role_id):
    try:
        event = Event.objects.by_slug(event_slug)
        role = EventRole.objects.get(id=role_id, event=event)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except EventRole.DoesNotExist:
        return render(request, "core/error.html", {"message": "Role not found"})
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    role.delete()
    messages.success(request, "Role has been deleted.", extra_tags="success")
    return redirect('role-list', event_slug=event_slug)

# RSVP Views
# =============================================================================

@user_has_role("event_manager")
def rsvp_list(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    paid_filter = request.GET.get('paid')
    if paid_filter is not None:
        if paid_filter.lower() == 'true':
            paid_filter = True
        elif paid_filter.lower() == 'false':
            paid_filter = False
        else:
            paid_filter = None

    rsvps = Rsvp.objects.by_event(event).filter_by_paid_status(paid_filter)

    context = {
        "event": event,
        "rsvps": rsvps,
    }
    return render(request, "rsvps/rsvp_list.html", context)

def rsvp_create(request, event_slug, role_id=None):
    try:
        event = Event.objects.by_slug(event_slug)
        if role_id:
            role = EventRole.objects.get(id=role_id, event=event)
        else:
            role = None
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except EventRole.DoesNotExist:
        return render(request, "core/error.html", {"message": "Role not found"})
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    if request.method == "POST":
        form = RsvpForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.role = role
            rsvp.save()

            # Handle payment if needed
            if event.payment_required:
                pass
            
            messages.success(request, "Registration was successful.", extra_tags="success")
            return redirect('rsvp-success', event_slug=event_slug, rsvp_slug=rsvp.slug)
    else:
        form = RsvpForm()

    context = {
        "form": form,
        "event": event,
        "role": role
    }
    return render(request, "rsvps/rsvp_form.html", context)

@user_has_role("event_manager")
def rsvp_detail(request, event_slug, rsvp_slug):
    try:
        event = Event.objects.by_slug(event_slug)
        rsvp = Rsvp.objects.by_event_and_slug(event, rsvp_slug)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "core/error.html", {"message": "RSVP not found"})
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    can_manage = check_user(request.user, "event_manager")
    
    context = {
        "rsvp": rsvp,
        "event": event,
        "can_manage": can_manage,
    }

    return render(request, "rsvps/rsvp_detail.html", context)

@user_has_role("event_manager")
def rsvp_update(request, event_slug, rsvp_slug):
    try:
        event = Event.objects.by_slug(event_slug)
        rsvp = Rsvp.objects.by_event_and_slug(event, rsvp_slug)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "core/error.html", {"message": "RSVP not found"})
    except Exception as e:
        return render(request, "core/error.html", {"message": str(e)})

    if request.method == "POST":
        form = UpdateRsvpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rsvp-list', event_slug=event.slug)
    else:
        form = UpdateRsvpForm(instance=rsvp)

    context = {
        "form": form,
        "event": event,
        "rsvp": rsvp,
    }
    return render(request, "rsvps/rsvp_update.html", context)

@user_has_role("event_manager")
def rsvp_delete(request, event_slug, rsvp_slug):
    try:
        event = Event.objects.by_slug(event_slug)
        rsvp = Rsvp.objects.by_event_and_slug(event, rsvp_slug)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "core/error.html", {"message": "RSVP not found"})
    except Exception as e:
        message = e
        return render(request, "core/error.html", {"message": message})
    
    if request.method == "POST":
        rsvp.delete()
        return redirect("rsvp-list")
    
    context = {
        'event': event,
        'rsvp': rsvp
    }
    return render(request, "rsvps/rsvp_delete_confirm.html", context)

def rsvp_success(request, event_slug, rsvp_slug):
    try:
        event = Event.objects.by_slug(event_slug)
        rsvp = Rsvp.objects.by_event_and_slug(event, rsvp_slug)
    except Event.DoesNotExist:
        return render(request, "core/error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "core/error.html", {"message": "RSVP not found"})
    except Exception as e:
        return render(request, "core/error.html", {"message": str(e)})

    context = {
        "event": event,
        "rsvp": rsvp
    } 
    return render(request, "rsvps/rsvp_success.html", context)

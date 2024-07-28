from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .models import Event, EventRole, Rsvp
from .forms import EventForm, EventRoleForm, RsvpForm, UpdateRsvpForm
from core.decorator import user_has_role, is_staff_or_trainer, is_staff
from core.utils import check_user, get_object_or_error
import stripe

# Stripe Setup
stripe.api_key = settings.STRIPE_TEST_SECRET

# Event Views
# =============================================================================

def event_list(request):
    # get all events
    events = Event.objects.all()

    # filter on event type
    event_type = request.GET.get("type")
    if event_type and event_type != 'all':
        events = events.filter_by_event_type(event_type)

    # filter on event status    
    event_status = request.GET.get("event_status")
    if event_status == "featured":
        events = events.featured()

    # only show upcoming events
    events = events.upcoming()

    context = {
        "type": event_type,
        "events": events,
    }
    return render(request, "events/event_list.html", context)

def event_detail(request, slug):
    event = get_object_or_error(request,Event, slug=slug)
    roles = event.roles.all()

    context = {
        "event": event, 
        "roles": roles,
    }
    return render(request, "events/event_detail.html", context)

@is_staff
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("event-list"))
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {"form": form})

@is_staff
def event_update(request, slug):
    event = get_object_or_error(request,Event, slug=slug)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', slug=event.slug)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_update.html", {"form": form})

@is_staff
def event_delete(request, slug):
    event = get_object_or_error(request,Event, slug=slug)
    
    if request.method == "POST":
        event.delete()
        return redirect("event-list")
    
    return render(request, "events/event_delete_confirm.html", {"event": event})

@is_staff
def role_create(request, event_slug):
    event = get_object_or_error(request,Event, slug=event_slug)
    
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

@is_staff
def role_list(request, event_slug):
    event = get_object_or_error(request,Event, slug=event_slug)
    roles = event.roles.all()

    context = {
        "event": event, 
        "roles": roles,
    }

    return render(request, "roles/role_list.html", context)

@user_has_role("event_manager")
def role_delete(request, event_slug, role_id):
    event = get_object_or_error(request,Event, slug=event_slug)
    role = get_object_or_error(request,EventRole, id=role_id, event=event)
    
    role.delete()
    messages.success(request, "Role has been deleted.", extra_tags="success")
    return redirect('role-list', event_slug=event_slug)

# RSVP Views
# =============================================================================

@is_staff
def rsvp_list(request, event_slug):
    event = get_object_or_error(request,Event, slug=event_slug)
    
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
                # Create Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': role.name if role else 'Event Registration',
                            },
                            'unit_amount': int(role.cost * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(
                        reverse('rsvp-success', args=[event_slug, rsvp.slug])
                    ),
                    cancel_url=request.build_absolute_uri(
                        reverse('rsvp-cancel', args=[event_slug, rsvp.slug])
                    ),
                )
                return redirect(session.url, code=303)
            
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

@is_staff
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

@is_staff
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

@is_staff
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
        return redirect("rsvp-list", event_slug=event_slug)
    
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
    
    rsvp.has_paid = True
    rsvp.save()
    messages.success(request, "Registration and payment were successful.", extra_tags="success")

    context = {
        "event": event,
        "rsvp": rsvp
    } 
    return render(request, "rsvps/rsvp_success.html", context)

def rsvp_cancel(request, event_slug, rsvp_slug):
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
    return render(request, "rsvps/rsvp_cancel.html", context)

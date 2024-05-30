from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Event, Rsvp
from .forms import EventForm, RsvpForm, RsvpFormNoPayment
from .decorator import user_has_role
from core.utils import check_user


# Event Views
# =============================================================================

def event_list(request):
    """
    Renders a list of events, including featured and upcoming events.

    Parameters:
    - request: HTTP request object

    Returns:
    - Rendered HTML template with event list
    """
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
    """
    Renders the detail page for a specific event.

    Parameters:
    - request: HTTP request object
    - slug: Slug of the event to display details for

    Returns:
    - Rendered HTML template with event details
    """
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    can_manage = check_user(request.user, "event_manager")
        
    context = {
        "event": event, 
        "can_manage": can_manage
    }
    return render(request, "events/event_detail.html", context)

@user_has_role("event_manager")
def event_create(request):
    """
    Handles the creation of a new event.

    Parameters:
    - request: HTTP request object

    Returns:
    - Rendered HTML template for event creation form
    - Redirects to event list on successful form submission
    """
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
    """
    Handles the update of an existing event.

    Parameters:
    - request: HTTP request object
    - slug: Slug of the event to update

    Returns:
    - Rendered HTML template for event update form
    - Redirects to event detail page on successful form submission
    """
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})

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
    """
    Handles the deletion of an existing event.

    Parameters:
    - request: HTTP request object
    - slug: Slug of the event to delete

    Returns:
    - Rendered HTML template for event deletion confirmation
    - Redirects to event list on successful deletion
    """
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    if request.method == "POST":
        event.delete()
        return redirect("event-list")
    
    return render(request, "events/event_delete_confirm.html", {"event": event})

# RSVP Views
# =============================================================================

@user_has_role("event_manager")
def rsvp_list(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
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

def rsvp_create(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    if request.method == "POST":
        if event.payment_required:
            form = RsvpForm(request.POST, event=event)
        else:
            form = RsvpFormNoPayment(request.POST, event=event)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.save()

            # Handle payment if needed
            rsvp_data = form.cleaned_data
            if event.payment_required:
                pass
        
            return redirect('event-detail', slug=event_slug)
    else:
        if event.payment_required:
            form = RsvpForm(event=event)
        else:
            form = RsvpFormNoPayment(event=event)

    context = {
        "form": form,
        "event": event
    }
    return render(request, "rsvps/rsvp_form.html", context)

@user_has_role("event_manager")
def rsvp_detail(request, event_slug, rsvp_slug):
    try:
        event = Event.objects.by_slug(event_slug)
        rsvp = Rsvp.objects.by_event_and_slug(event, rsvp_slug)
    except Event.DoesNotExist:
        return render(request, "events/event_error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "events/event_error.html", {"message": "RSVP not found"})
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
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
        return render(request, "events/event_error.html", {"message": "Event not found"})
    except Rsvp.DoesNotExist:
        return render(request, "events/event_error.html", {"message": "RSVP not found"})
    except Exception as e:
        return render(request, "events/event_error.html", {"message": str(e)})

    if request.method == "POST":
        form = RsvpFormNoPayment(request.POST, instance=rsvp, event=event)
        if form.is_valid():
            form.save()
            return redirect('rsvp-detail', event_slug=event_slug, rsvp_slug=rsvp_slug)
    else:
        form = RsvpFormNoPayment(instance=rsvp, event=event)

    context = {
        "form": form,
        "event": event,
        "rsvp": rsvp,
    }
    return render(request, "rsvps/rsvp_update.html", context)


    
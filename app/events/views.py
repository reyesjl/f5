from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Event, Rsvp
from .forms import EventForm, RSVPStatusCheckForm, RsvpForm, RsvpFormNoPayment
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
    featured_events = Event.objects.featured()
    upcoming_events = Event.objects.upcoming().exclude(featured=True)

    context = {
        "featured_events": featured_events,
        "upcoming_events": upcoming_events,
    }
    return render(request, "events/event_list.html", context)

def events_by_type(request, event_type):
    """
    Renders a list of events filtered by event type.

    Parameters:
    - request: HTTP request object
    - event_type: Type of events to filter by

    Returns:
    - Rendered HTML template with filtered event list
    """
    events = Event.objects.by_type(event_type)

    context = {
        "events": events,
        "event_type": event_type,
    }
    return render(request, "events/filtered_event_list.html", context)

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
def rsvp_by_event(request, event_slug):
    try:
        event = Event.objects.by_slug(event_slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    rsvps = Rsvp.objects.by_event(event)

    context = {
        "event": event,
        "rsvps": rsvps,
    }
    return render(request, "rsvps/rsvp_by_event.html", context)

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
def rsvp_detail(request, slug):
    try:
        rsvp = Rsvp.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    context = {
        "rsvp": rsvp,
    }

    return render(request, "rsvps/rsvp_detail.html", context)
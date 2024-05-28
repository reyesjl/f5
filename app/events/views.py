from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Event, Rsvp
from .forms import EventForm, RsvpForm
from .decorator import user_has_role
from core.utils import check_user


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
            return redirect(reverse("event-list"))  # Redirect to the events list or any other view
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
            return redirect('event-detail', slug=event.slug)  # Redirect to the event detail page
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_update.html", {"form": form})

@user_has_role("event_manager")
def event_delete(request, slug):
    try:
        event = Event.objects.by_slug(slug)
    except Exception as e:
        message = e
        return render(request, "events/event_error.html", {"message": message})
    
    if request.method == "POST":
        event.delete()
        return redirect("event-list")
    
    return render(request, "events/event_delete_confirm.html", {"event": event})
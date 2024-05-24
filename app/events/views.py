from django.shortcuts import render
from django.http import HttpResponse
from .models import Event


def index(request):
    upcoming_events = Event.objects.upcoming_events()
    
    context = {'events': upcoming_events}

    return render(request, 'events/index.html', context)

def event_details(request, event_id):
    event = Event.objects.by_event_id(event_id)

    context = {'event': event}

    return render(request, 'events/event_details.html', context)

def events_by_type(request, event_type):
    events_by_type = Event.objects.upcoming_events().by_event_type(event_type)
    
    context = {
        'events': events_by_type,
        'event_type': event_type
    }

    return render(request, 'events/events_by_type.html', context)
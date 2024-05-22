from django.shortcuts import render
from django.http import HttpResponse
from .models import Event

def index(request):
    upcoming_events = Event.objects.upcoming_events()

    context = {
        'upcoming_events': upcoming_events,
    }
    
    return render(request, 'events/index.html', context)
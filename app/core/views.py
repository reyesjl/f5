from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event

def index(request):
    events = Event.objects.all()
    events = events.upcoming().featured()[:5]

    context = {
        "events": events,
    }
    return render(request, 'core/index.html', context)
from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event
from health.models import Post
from django.contrib import messages

def index(request):
    events = Event.objects.upcoming().featured()[:5]
    posts = Post.objects.published().featured()[:5]

    # messages.add_message(request, messages.INFO, 'Welcome to First Five Rugby!', extra_tags='info')
    # messages.add_message(request, messages.SUCCESS, 'Your operation was successful.', extra_tags='success')
    # messages.add_message(request, messages.WARNING, 'This is a warning message.', extra_tags='warning')
    # messages.add_message(request, messages.ERROR, 'An error has occurred.', extra_tags='error')

    context = {
        "events": events,
        "posts": posts,
    }
    return render(request, 'core/index.html', context)
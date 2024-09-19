from django.shortcuts import redirect, render
from django.conf import settings
from .forms import EventSubmissionForm
from core.utils import check_user, get_object_or_error
import stripe

# Stripe Setup
stripe.api_key = settings.STRIPE_TEST_SECRET

def list_events(request):
    context = {}
    return render(request, "events/list_events.html", context)

def submit_event(request):
    if request.method == 'POST':
        form = EventSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "events/submit_event_success.html")
    else:
        form = EventSubmissionForm()

    context = {
        'form': form,
    }

    return render(request, "events/submit_event.html", context)
    
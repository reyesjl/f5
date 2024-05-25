from django.shortcuts import redirect, render
from .models import Event, Rsvp
from .forms import RsvpForm
from .decorator import validate_rsvp_token


def index(request):
    featured_events = Event.objects.upcoming_events().featured_events()
    upcoming_events = Event.objects.upcoming_events().exclude(featured=True)
    
    context = {
        'featured_events': featured_events,
        'upcoming_events': upcoming_events
    }

    return render(request, 'events/index.html', context)

def event_details(request, event_id):
    try:
        event = Event.objects.by_event_id(event_id)
    except Event.DoesNotExist:
        return render(request, 'events/event_not_found.html')

    context = {'event': event}

    return render(request, 'events/event_details.html', context)

def events_by_type(request, event_type):
    events_by_type = Event.objects.upcoming_events().by_event_type(event_type)
    
    context = {
        'events': events_by_type,
        'event_type': event_type
    }

    return render(request, 'events/events_by_type.html', context)

def rsvp_create(request, event_id):
    try:
        event = Event.objects.by_event_id(event_id)
    except Event.DoesNotExist:
        return render(request, 'events/event_not_found.html')
    
    if not event.registration_required:
        return render(request, 'events/rsvp_no_register.html', {'event':event})
    
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            cleaned_data = form.validate_rsvp(event)
            if form.errors:
                return render(request, 'events/rsvp_create.html', {'event': event, 'form': form})
            rsvp.save()
            return redirect('rsvp_receipt', token=rsvp.token)
    else:
        form = RsvpForm()
        
    context = {
        'event': event,
        'form': form
    }

    return render(request, 'events/rsvp_create.html', context)

@validate_rsvp_token
def rsvp_receipt(request, token):
    try:
        rsvp = Rsvp.objects.by_token(token)
    except Rsvp.DoesNotExist:
        return render(request, 'events/rsvp_not_found.html')
    
    payment_info = rsvp.payment_status_and_cost()
    
    context = {
        'rsvp': rsvp,
        'token': token,
        'payment_info': payment_info,
    }

    return render(request, 'events/rsvp_receipt.html', context)

@validate_rsvp_token
def generate_pdf(request, token):
    try:
        rsvp = Rsvp.objects.by_token(token)
    except Rsvp.DoesNotExist:
        return render(request, 'events/rsvp_not_found.html')

    pdf_response = rsvp.generate_pdf_receipt()

    # If you want to return the PDF directly
    return pdf_response
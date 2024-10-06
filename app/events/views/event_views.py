from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from ..models import Event
from ..forms import EventForm
from core.decorators import is_admin

class EventListView(ListView):
    model = Event
    template_name = 'events/list_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all()

@method_decorator(user_passes_test(is_admin), name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('list_events')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail_event.html'
    context_object_name = 'event'

@method_decorator(user_passes_test(is_admin), name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/update_event.html'
    success_url = reverse_lazy('list_events')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('list_events')

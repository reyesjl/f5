from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView, ListView
from ..models import EventSubmission
from ..forms import EventSubmissionForm
from core.decorators import is_admin


@method_decorator(user_passes_test(is_admin), name='dispatch')
class EventSubmissionListView(ListView):
    model = EventSubmission
    template_name = 'events/event_submissions/list_event_submissions.html'
    context_object_name = 'list_event_submissions'

class EventSubmissionCreateView(CreateView):
    model = EventSubmission
    form_class = EventSubmissionForm
    template_name = 'events/event_submissions/create_event_submission.html'
    success_url = reverse_lazy('list_events')
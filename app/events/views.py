import stripe
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from .forms import EventSubmissionForm
from .models import EventSubmission
from django.contrib.auth.decorators import login_required, user_passes_test
from core.decorators import is_admin
from django.contrib import messages
from django.core.paginator import Paginator

# Stripe Setup
stripe.api_key = settings.STRIPE_TEST_SECRET


def list_events(request):
    context = {}
    return render(request, "events/list_events.html", context)


def submit_event(request):
    if request.method == "POST":
        form = EventSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "events/submit_event_success.html")
    else:
        form = EventSubmissionForm()

    context = {
        "form": form,
    }

    return render(request, "events/submit_event.html", context)


@user_passes_test(is_admin)
def list_submissions(request):
    submissions_list = EventSubmission.objects.all().order_by('event_date')
    paginator = Paginator(submissions_list, 10)

    page_number = request.GET.get('page')
    submissions = paginator.get_page(page_number)

    context = {
        "submissions": submissions,
        "paginator": paginator,
    }
    return render(request, "events/list_submissions.html", context)


@user_passes_test(is_admin)
def update_submission_status(request, submission_id, action):
    submission = get_object_or_404(EventSubmission, id=submission_id)

    if action == 'change' and request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Ensure the new status is valid
        if new_status in dict(submission.SUBMISSION_STATUS_CHOICES).keys():
            submission.internal_status = new_status
            submission.save()
            messages.success(request, f'Submission status updated to {new_status}')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('list_submissions')

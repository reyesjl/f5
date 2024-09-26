from .models import Plan
from django.shortcuts import redirect, render
from core.decorators import is_admin
from .forms import TrainerRequestForm, CreatePlanForm
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import user_passes_test

# Trainers
VALID_TRAINERS = ['Cuyler', 'Asau']

def index(request):
    plans = Plan.objects.all()

    context = {
        'plans': plans
    }
    return render(request, "health/index.html", context)

def request_trainer(request, trainer_name):
    # Check trainer name
    if trainer_name not in VALID_TRAINERS:
        return render(request, 'health/request_trainer_error.html')
    
    if request.method == 'POST':
        form = TrainerRequestForm(request.POST)
        if form.is_valid():
            trainer_request = form.save(commit=False)
            trainer_request.trainer_name = trainer_name
            trainer_request.save()

            # Create email
            # TO FIX : EMAIL SHIT
            # email = EmailMessage(
            #     subject=f"New Trainer Request for {trainer_name}",
            #     body=f"{trainer_request.name} ({trainer_request.email}) has requested to chat with {trainer_name}. Message: {trainer_request.message}",
            #     from_email='support@f5rugby.com',
            #     to=['support@f5rugby.com'],
            #     reply_to=[trainer_request.email],
            # )
            # # Send notification email
            # email.send()
            return render(request, 'health/request_trainer_success.html')
    else:
        form = TrainerRequestForm()
    
    context = {
        'form': form,
        'trainer_name': trainer_name
    }

    return render(request, 'health/request_trainer.html', context)

@user_passes_test(is_admin)
def create_plan(request):
    if request.method == "POST":
        form = CreatePlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('health_index')
    else:
        form = CreatePlanForm()
    
    context = {
        'form': form
    }
    return render(request, "health/create_plan.html", context)

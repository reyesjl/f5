from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from .forms import TrainerRequestForm
from .models import TrainerRequest

# Trainers
VALID_TRAINERS = ['Cuyler', 'Asau']

def index(request):
    context = {}
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
            email = EmailMessage(
                subject=f"New Trainer Request for {trainer_name}",
                body=f"{trainer_request.name} ({trainer_request.email}) has requested to chat with {trainer_name}. Message: {trainer_request.message}",
                from_email='support@f5rugby.com',
                to=['support@f5rugby.com'],
                reply_to=[trainer_request.email],
            )
            # Send notification email
            email.send()
            return render(request, 'health/request_trainer_success.html')
    else:
        form = TrainerRequestForm()
    
    context = {
        'form': form,
        'trainer_name': trainer_name
    }

    return render(request, 'health/request_trainer.html', context)

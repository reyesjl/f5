from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm, TourInquiryForm
from .models import TourInquiry

def index(request):
    context = {}
    return render(request, 'core/index.html', context)

def tours(request):
    context = {}
    return render(request, 'core/tours.html', context)

def tour_inquiry(request):
    if request.method == 'POST':
        form = TourInquiryForm(request.POST)
        if form.is_valid:
            form.save()
            return render(request, "core/tour_inquiry_success.html")
    else:
        form = TourInquiryForm()
    
    context = {
        'form': form
    }
    return render(request, "core/tour_inquiry.html", context)

def privacy(request):
    context = {}
    return render(request, 'core/privacy_policy.html', context)

def terms_of_use(request):
    context = {}
    return render(request, 'core/terms_of_use.html', context)

def sales_and_refunds(request):
    context = {}
    return render(request, 'core/sales_and_refunds.html', context)

def legal(request):
    context = {}
    return render(request, 'core/legal.html', context)

def sitemap(request):
    context = {}
    return render(request, 'core/sitemap.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create email
            email = EmailMessage(
                subject=f"Message from {form.cleaned_data['name']}",
                body=form.cleaned_data['message'],
                from_email='support@f5rugby.com',
                to=['support@f5rugby.com'],
                reply_to=[form.cleaned_data['email']],
            )
            # Send notification email
            email.send()
            return render(request, 'core/contact_success.html')
    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    return render(request, 'core/contact.html', context)
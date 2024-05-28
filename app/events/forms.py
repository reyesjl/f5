from django import forms
from .models import Event, Rsvp
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'detailed_description', 'event_type',
            'featured', 'start_date', 'end_date', 'location',
            'registration_required', 'payment_required', 'cost',
            'cost_secondary'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'description': 'Preview description',
            'detailed_description': 'Detailed description',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'End date cannot be before start date.')
            if start_date < timezone.now():
                self.add_error('start_date', 'Start date cannot be in the past.')

class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = [
            'name',
            'email',
            'phone_number',
            'role'
        ]

    def validate_rsvp(self, event):
        print("VALIDATING...................")
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        if Rsvp.objects.email_exists_for_event(event, email=email):
            self.add_error('email', 'An RSVP already exists with this email.')
        if Rsvp.objects.phone_exists_for_event(event, phone_number=phone_number):
            self.add_error('phone_number', 'An RSVP already exists with this phone number.')

        return cleaned_data

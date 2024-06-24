from django import forms
from .models import Event, EventRole, Rsvp
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'detailed_description', 'event_type',
            'featured', 'start_date', 'end_date', 'location',
            'registration_required', 'payment_required'
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

class EventRoleForm(forms.ModelForm):
    class Meta:
        model = EventRole
        fields = [
            'name', 'cost'
        ]

class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = [
            'name',
            'email',
            'phone_number'
        ]
    
class UpdateRsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = [
            'name',
            'email',
            'phone_number',
            'has_paid'
        ]
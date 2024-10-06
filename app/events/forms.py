from django import forms
from .models import Event, EventSubmission

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'start_date',
            'end_date',
            'location',
        ]

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class EventSubmissionForm(forms.ModelForm):
    class Meta:
        model = EventSubmission
        fields = [
            "event_name",
            "event_description",
            "event_date",
            "name",
            "email",
            "phone_number",
        ]

        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
        }

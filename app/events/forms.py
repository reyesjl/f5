from django import forms
from .models import Event, EventSubmission


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

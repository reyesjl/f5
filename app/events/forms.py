from django import forms
from .models import Rsvp

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

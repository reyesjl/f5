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
    credit_card_number = forms.CharField(max_length=16)
    full_name_on_card = forms.CharField(max_length=255)
    expiration_month = forms.CharField(max_length=2, label='Expiration month')
    expiration_year = forms.CharField(max_length=4, label='Expiration year')
    cvv = forms.CharField(max_length=4)

    class Meta:
        model = Rsvp
        fields = [
            'name',
            'email',
            'phone_number',
            'role'
        ]

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_credit_card_number(self):
        credit_card_number = self.cleaned_data.get('credit_card_number')
        if not credit_card_number.isdigit():
            self.add_error('credit_card_number', "Credit card number must contain only digits.")
        return credit_card_number

    def clean_expiration_month(self):
        expiration_month = self.cleaned_data.get('expiration_month')
        if not expiration_month.isdigit() or not (1 <= int(expiration_month) <= 12):
            self.add_error('expiration_month', "Expiration month must be a number between 01 and 12.")
        return expiration_month

    def clean_expiration_year(self):
        expiration_year = self.cleaned_data.get('expiration_year')
        current_year = timezone.now().year
        if not expiration_year.isdigit() or not (current_year <= int(expiration_year) <= current_year + 20):
            self.add_error('expiration_year', f"Expiration year must be a number between {current_year} and {current_year + 20}.")
        return expiration_year

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit():
            self.add_error('cvv', "CVV must contain only digits.")
        if len(cvv) not in [3, 4]:
            self.add_error('cvv', "CVV must be either 3 or 4 digits long.")
        return cvv
    
    def clean_role(self):
        role = self.cleaned_data.get('role')
        if self.event and self.event.event_type == 'game' and role in ['player', 'coach']:
            self.add_error('role', "Players and coaches cannot register for game events.")
        return role

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.event and not self.instance:  # Check if creating a new instance
            if Rsvp.objects.email_exists_for(self.event, email=email):
                self.add_error('email', 'An RSVP already exists with this email.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if self.event and not self.instance:  # Check if creating a new instance
            if Rsvp.objects.phone_exists_for(self.event, phone_number=phone_number):
                self.add_error('phone_number', 'An RSVP already exists with this phone number.')
        return phone_number
    
class RsvpFormNoPayment(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = [
            'name',
            'email',
            'phone_number',
            'role'
        ]

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if self.event and self.event.event_type == 'game' and role in ['player', 'coach']:
            self.add_error('role', "Players and coaches cannot register for game events.")
        return role

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.event and not self.instance:  # Check if creating a new instance
            if Rsvp.objects.email_exists_for(self.event, email=email):
                self.add_error('email', 'An RSVP already exists with this email.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if self.event and not self.instance:  # Check if creating a new instance
            if Rsvp.objects.phone_exists_for(self.event, phone_number=phone_number):
                self.add_error('phone_number', 'An RSVP already exists with this phone number.')
        return phone_number
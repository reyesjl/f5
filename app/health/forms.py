from django import forms
from .models import TrainerRequest

class TrainerRequestForm(forms.ModelForm):
    class Meta:
        model = TrainerRequest
        fields = ['name', 'email', 'phone_number', 'message']
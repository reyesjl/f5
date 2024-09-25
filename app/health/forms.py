from django import forms
from .models import TrainerRequest, Plan

class TrainerRequestForm(forms.ModelForm):
    class Meta:
        model = TrainerRequest
        fields = ['name', 'email', 'phone_number', 'message']

class CreatePlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'trainer_name', 'pdf', 'goal']
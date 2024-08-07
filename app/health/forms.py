from django import forms
from .models import Plan, HealthProfile, TrainerSessionRequest

class PlanForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        help_text='Tags must be comma seperated.',
        widget=forms.TextInput(attrs={'placeholder': 'Tag1, Tag2, Tag3'}),
        required=False
    )

    class Meta:
        model = Plan
        fields = [
            'title', 'type', 'featured', 'excerpt', 'document',
            'tags', 'featured_image', 'status',
        ]

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ['height', 'weight', 'squat', 'bench', 'chin_up', 'deadlift', 'bronco', 'broad_jump', 'vertical', 'forty_meter_sprint']
        widgets = {
            'bronco': forms.TextInput(attrs={'placeholder': 'HH:MM'}),
            'height': forms.NumberInput(attrs={'placeholder': '71.3'}),
            'weight': forms.NumberInput(attrs={'placeholder': '185.3'}),
            'squat': forms.NumberInput(attrs={'placeholder': '315'}),
            'bench': forms.NumberInput(attrs={'placeholder': '225'}),
            'chin_up': forms.NumberInput(attrs={'placeholder': '14'}),
            'deadlift': forms.NumberInput(attrs={'placeholder': '405'}),
            'broad_jump': forms.NumberInput(attrs={'placeholder': '43.2'}),
            'vertical': forms.NumberInput(attrs={'placeholder': '30.2'}),
            'forty_meter_sprint': forms.NumberInput(attrs={'placeholder': '5.2'}),
        }
        help_texts = {
            'height': 'Enter height in inches.',
            'weight': 'Enter weight in lbs.',
            'squat': 'Enter squat max in lbs.',
            'bench': 'Enter bench press max in lbs.',
            'chin_up': 'Enter number of chin-ups.',
            'deadlift': 'Enter deadlift max in lbs.',
            'bronco': 'Enter time duration in HH:MM format.',
            'broad_jump': 'Enter broad jump distance in inches.',
            'vertical': 'Enter vertical jump height in inches.',
            'forty_meter_sprint': 'Enter 40-meter sprint time in seconds.',
        }

class TrainerSessionRequestForm(forms.ModelForm):
    class Meta:
        model = TrainerSessionRequest
        fields = ['requested_date', 'requested_time', 'additional_details']
        widgets = {
            'requested_date': forms.DateInput(attrs={'type': 'date'}),
            'requested_time': forms.TimeInput(attrs={'type': 'time'}),
            'additional_details': forms.Textarea(attrs={'rows': 4}),
        }
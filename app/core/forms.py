from django import forms
from .models import TourInquiry

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class TourInquiryForm(forms.ModelForm):
    class Meta:
        model = TourInquiry
        fields = ['name', 'phone', 'email', 'num_people']

        labels = {
            'num_people': 'Number of Participants',
        }

        widgets = {
            'num_people': forms.NumberInput(attrs={'placeholder': 'Number of People'}),
        }

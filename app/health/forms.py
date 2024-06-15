from django import forms
from .models import Plan

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
            'title', 'author', 'type', 'featured', 'excerpt', 'content', 
            'tags', 'featured_image', 'status', 'reading_time'
        ]

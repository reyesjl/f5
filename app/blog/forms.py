from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        help_text='Tags must be comma seperated.',
        widget=forms.TextInput(attrs={'placeholder': 'Tag1, Tag2, Tag3'}),
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'title', 'type', 'featured', 'excerpt', 'content', 
            'tags', 'visibility', 'reading_time'
        ]
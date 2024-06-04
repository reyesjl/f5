from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'author', 'featured', 'excerpt', 'content', 
            'tags', 'featured_image', 'status', 'reading_time', 
            'views', 'likes'
        ]

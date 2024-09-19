from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

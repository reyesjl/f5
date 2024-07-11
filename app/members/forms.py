from django import forms
from .models import CustomUser, SupportTicket
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class MemberAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['email', 'subject', 'message']
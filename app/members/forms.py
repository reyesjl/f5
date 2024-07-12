from django import forms
from .models import CustomUser, SupportTicket
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'is_staff', 'is_trainer', 'bio']

class MemberAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['email', 'subject', 'message']

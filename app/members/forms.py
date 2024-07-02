from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class MemberAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
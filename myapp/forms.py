from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# inherit UserCreationForm to create SignupForm
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input-text",
                "autocomplete":"email",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password",
            }
        )
    )
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        

# create a login form
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input-text",
                "autocomplete":"email",
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password",
                "autocomplete":"password",
                "placeholder": "Enter your password",
            }
        )
    )


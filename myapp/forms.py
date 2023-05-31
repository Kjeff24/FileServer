from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
                "class": "input-text",
                "id":"passwordField1"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-text",
                "id":"passwordField2"
            }
        )
    )
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        

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
                "class": "login-input",
                "id":"passwordField",
                "autocomplete":"password",
                "placeholder": "Enter your password",
            }
        )
    )


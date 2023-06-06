from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# inherit UserCreationForm to create SignupForm
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input-text form-control",
                "autocomplete":"email",
                'id':"floatingInput",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password form-control",
                'id':"floatingInput1",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password form-control",
                'id':"floatingInput2",
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
                "class": "input-text form-control",
                "autocomplete":"email",
                'id':"floatingInput",
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "toggleable-password form-control",
                "autocomplete":"password",
                "placeholder": "Enter your password",
                "id":"floatingPassword",
            }
        )
    )


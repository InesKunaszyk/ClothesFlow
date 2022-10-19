from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm

from .models import User

User = get_user_model()


# class UserCreateForm(UserCreationForm):
#     name = forms.CharField(max_length=50)
#     surname = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Podaj hasło')
#     password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Powtórz hasło')
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'password', 'password2')

class UserCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField(required=True, empty_value=False)
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Podaj hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Powtórz hasło')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def clean(self):
        cd = super().clean()
        pass1 = cd.get("password")
        pass2 = cd.get("password2")
        if pass1 != pass2:
            raise ValidationError("Hasła nie są takie same! Popraw dane.")


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        email = cd.get("email")
        password = cd.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError("Nieprawidłowe dane logowania")
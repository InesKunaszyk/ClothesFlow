from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.contrib.auth.forms import UserCreationForm

from .models import User, Category, Institution, Donation

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
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


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = forms.CharField()
    surname = forms.CharField
    email = forms.EmailField(required=True, validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class NewDonationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    bag = forms.IntegerField()
    institution = forms.ModelChoiceField(queryset=Institution.objects.all())
    address = forms.CharField()
    city = forms.CharField()
    zip_code = forms.CharField()
    phone_number = forms.IntegerField()
    date = forms.DateField()
    time = forms.TimeField()
    more_info = forms.Textarea()

    class Meta:
        model = Donation
        fields = ('categories', 'bag', 'institution', 'address', 'city', 'zip_code', 'phone_number', 'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user')
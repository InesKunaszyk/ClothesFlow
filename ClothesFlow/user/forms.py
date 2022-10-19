from django.contrib.auth.forms import UserCreationForm

from models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password', 'password2',)
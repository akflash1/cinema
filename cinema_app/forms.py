from django.contrib.auth.forms import UserCreationForm

from cinema_app.models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

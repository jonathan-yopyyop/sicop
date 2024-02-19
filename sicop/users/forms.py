from django import forms
from django.contrib.auth.forms import UserCreationForm

from sicop.users.models import User


# Sign Up Form
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=False,
        help_text="Username",
    )
    name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Name",
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Enter a valid email address",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "email",
            "password1",
            "password2",
        ]

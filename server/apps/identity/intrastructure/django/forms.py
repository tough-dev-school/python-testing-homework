from typing import final

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
)
from django.contrib.auth.forms import UserCreationForm

from server.apps.identity.models import User
from server.common.django.forms import DateWidget


@final
class RegistrationForm(UserCreationForm[User]):
    """Create user with all the contact details."""

    class Meta(object):
        model = User
        fields = (
            [User.USERNAME_FIELD] +
            User.REQUIRED_FIELDS +
            User.OPTIONAL_FIELDS
        )
        widgets = {
            User.USERNAME_FIELD: forms.EmailInput(),
            'date_of_birth': DateWidget(),
        }


@final
class AuthenticationForm(BaseAuthenticationForm):
    """Redefined default email widget."""

    username = forms.EmailField()


@final
class UserUpdateForm(forms.ModelForm[User]):
    """
    Update user with all the required details.

    Except passwords. Why?
    1. Passwords are hard to update
    2. You have to input the current password to set a new one
    3. We would need to notify user by email about the password change
    4. All sessions are killed, we will need to restore at least one manually
    5. We already have a change-password mechanics

    You also cannot change 'email': it is our main identifier.
    """

    class Meta(object):
        model = User
        fields = User.REQUIRED_FIELDS + User.OPTIONAL_FIELDS
        widgets = {
            'date_of_birth': DateWidget(),
        }

from django.http import HttpResponse
from django.shortcuts import render
from django.test import RequestFactory

from server.apps.identity.intrastructure.django.forms import RegistrationForm


def test_registration():
    """Test registration template."""
    page = render(
        RequestFactory().get('/identity/registration'),
        'identity/pages/registration.html',
        {
            'form': RegistrationForm(),
        },
    )

    assert isinstance(page, HttpResponse)

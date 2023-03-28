"""Test the views of the ``identity`` app."""
from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

pytestmark = pytest.mark.django_db


def test_login_view_get(client: Client) -> None:
    """Test accessing the LoginView with a GET request."""
    url = reverse('identity:login')
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert 'csrfmiddlewaretoken' in response.content.decode()
    assert isinstance(response.context['user'], AnonymousUser)


def test_login_view_post(client: Client, user_data: dict[str, str]) -> None:
    """Test submitting the login form with valid credentials."""
    User.objects.create_user(**user_data)
    url = reverse('identity:login')
    response = client.post(
        url,
        {'username': user_data['email'], 'password': user_data['password']},
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')


def test_registration_view_get(client: Client) -> None:
    """Test accessing the RegistrationView with a GET request."""
    url = reverse('identity:registration')
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert 'csrfmiddlewaretoken' in response.content.decode()
    assert isinstance(response.context['user'], AnonymousUser)


def test_registration_view_post(
    client: Client, user_data: dict[str, str],
) -> None:
    """Test submitting the registration form with valid data."""
    url = reverse('identity:registration')
    registration_data = user_data.copy()
    registration_data['password1'] = user_data['password']
    registration_data['password2'] = user_data['password']
    response = client.post(url, registration_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')
    assert User.objects.filter(email=user_data['email']).exists()

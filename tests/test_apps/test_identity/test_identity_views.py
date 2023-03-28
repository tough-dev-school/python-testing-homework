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
    assert response.get('Location', '') == reverse('pictures:dashboard')


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
    assert response.get('Location', '') == reverse('identity:login')
    assert User.objects.filter(email=user_data['email']).exists()


def test_user_update_view(client: Client, user_data: dict[str, str]) -> None:
    """Test accessing and updating the UserUpdateView."""
    user = User.objects.create_user(**user_data)
    client.force_login(user)

    url = reverse('identity:user_update')
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert 'csrfmiddlewaretoken' in response.content.decode()
    assert response.context['user'] == user

    # TODO: change for a fixture
    updated_data = {
        'first_name': 'UpdatedFirstName',
        'last_name': 'UpdatedLastName',
        'address': '123 Main St, Anytown',
        'job_title': 'Software Engineer',
        'phone': '+1 123-456-7890',
    }
    response = client.post(url, updated_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location', '') == reverse('identity:user_update')

    user.refresh_from_db()
    assert user.first_name == updated_data['first_name']
    assert user.last_name == updated_data['last_name']

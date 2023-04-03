from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        UserAssertion
    )


@pytest.mark.django_db()
def test_registration_page_renders(client: Client) -> None:
    """Basic `get` method works."""
    response = client.get(reverse("identity:registration"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data)


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    user_data: 'RegistrationData'
) -> None:
    """Save User model"""
    user = User(**user_data)
    user.save()

    """Get data for login"""
    login_data = {
        'username': user_data['email'],
        'password': user_data['password']
    }

    """Login"""
    client.force_login(user)

    """Check user login."""
    response = client.post(
        reverse('identity:login'),
        data=login_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')

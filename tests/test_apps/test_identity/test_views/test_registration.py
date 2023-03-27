from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from tests.plugins.identity.user import (
        UserDetails,
        UserDetailsAssertion,
        UserRegisterDetails,
    )

pytestmark = [
    pytest.mark.django_db,
]


def test_registration_success(
    client: 'Client',
    user_details: 'UserDetails',
    user_register_details: 'UserRegisterDetails',
    assert_user_details: 'UserDetailsAssertion',
):
    """Test user registration success."""
    email = user_register_details['email']

    response = client.post(
        reverse('identity:registration'),
        data=user_register_details,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('location') == reverse('identity:login')
    assert_user_details(email, user_details)


def test_registration_different_passwords_error(
    client: 'Client',
    user_register_details: 'UserRegisterDetails',
):
    """Test user registration with different passwords, error."""
    user_register_details['password1'] = 'first'
    user_register_details['password2'] = 'second'

    response = client.post(
        reverse('identity:registration'),
        data=user_register_details,
    )

    assert response.status_code == HTTPStatus.OK
    assert 'password2' in response.context['form'].errors


def test_registration_invalid_email_error(
    client: 'Client',
    user_register_details: 'UserRegisterDetails',
    invalid_email: str,
):
    """Test user registration with invalid email, error."""
    user_register_details['email'] = invalid_email

    response = client.post(
        reverse('identity:registration'),
        data=user_register_details,
    )

    assert response.status_code == HTTPStatus.OK
    assert 'email' in response.context['form'].errors

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'field',
    User.REQUIRED_REGISTRATION_FIELDS + [User.USERNAME_FIELD, 'password1', 'password2'],
)
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(
        **{field: ''},  # type: ignore[arg-type]
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_empty_birthday(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that missing date of birth will not fail registration"""
    post_data = registration_data_factory(
        **{'date_of_birth': ''},  # type: ignore[arg-type]
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    user = User.objects.get(email=post_data['email'])
    assert user.date_of_birth is None


@pytest.mark.django_db()
def test_not_valid_email(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that not valid email will not fail registration"""
    post_data = registration_data_factory(
        **{'email': 'wrong_email'},  # type: ignore[arg-type]
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.context['form'].errors
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_user_already_exists(
    client: Client,
    db_user: 'UserData',
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    post_data = registration_data_factory(
        **db_user,
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.context['form'].errors
    assert response.status_code == HTTPStatus.OK

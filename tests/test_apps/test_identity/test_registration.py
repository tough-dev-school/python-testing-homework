from typing import TYPE_CHECKING

from http import HTTPStatus

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


@pytest.fixture()
def expected_user_data(
    registration_data: 'RegistrationData',
) -> 'UserData':
    """Expectd data for a Registrered user."""
    return {  # type: ignore[return-value]
            key_name: value_part
            for key_name, value_part in registration_data.items()
            if not key_name.startswith('password')
        }


@pytest.mark.django_db()
def test_registration_page_renders(client: Client) -> None:
    """Basic `get` method works."""

    response = client.get(reverse('identity:registration'))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], expected_user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(
        **{field: ''}, # type: ignore[arg-type]
    )

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ('invalid_field', 'invalid_value'), [
        ('email', 'wrong@email'),
        ('date_of_birth', '2000-02-30'),
        ('date_of_birth', '321123'),
    ]
)
def test_registration_invalid_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    invalid_field: str,
    invalid_value: str,
) -> None:
    """Tests that invalid field value will fail registration process."""
    post_data = registration_data_factory(
        **{invalid_field: invalid_value}, # type: ignore[arg-type]
    )

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.exists()

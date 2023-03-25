from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field

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
    expected_user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with valid data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], expected_user_data)


@pytest.mark.django_db()
def test_invalid_registration(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test that registration fails with invalid data."""
    post_data = registration_data_factory(email='invalid_email')
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.context['form'].errors == {
        'email': ['Введите правильный адрес электронной почты.'],
    }
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that registration fails without required field."""
    post_data = registration_data_factory(**{field: ''})
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.context['form'].errors == {
        field: ['Обязательное поле.'],
    }
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_update_user(
    registration_data: 'RegistrationData',
    logged_in_client: Client,
    mimesis_field: Field,
) -> None:
    """Test that user can update userinfo."""

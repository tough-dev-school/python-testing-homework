from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.test_apps.test_identity.conftest import (
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
    assert_correct_user(registration_data['email'], user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
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
    assert response.context['form'].errors == {
        field: ['Обязательное поле.'],
    }
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_invalid_login(client: Client, user: User) -> None:
    """Test that registration works with correct user data."""
    invalid_password = 'invalid_password'  # noqa: S105
    response = client.post(
        reverse('identity:login'),
        data={
            'username': user.email,
            'password': invalid_password,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.context['form'].errors == {
        '__all__': [
            'Пожалуйста, введите правильные email и пароль. Оба поля могут '
            'быть чувствительны к регистру.',  # noqa: WPS326
        ],
    }


@pytest.mark.django_db()
def test_update_user(
    user_data: 'UserData',
    user_client: Client,
    mimesis_field: Field,
) -> None:
    """Test that user can update info."""
    first_name = mimesis_field('person.first_name')
    user_data.update({
        'first_name': first_name,
    })
    response = user_client.post(
        reverse('identity:user_update'),
        data=user_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert User.objects.get(email=user_data['email']).first_name == first_name

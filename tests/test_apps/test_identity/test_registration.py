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

invalid_emails = [
    'plain_address',  # Простой адрес без @
    '@missing_username.com',  # Отсутствует имя пользователя перед @
    'username@.com',  # Отсутствует доменное имя после @
    'username@domain..com',  # Два точечных символа в домене
    'username@domain.com-',  # Домен заканчивается недопустимым символом
    'username@.domain.com',  # Домен начинается с точечного символа
    '.username@domain.com',  # Имя пользователя начинается с точечного символа
    'username@domain,com',  # Использует запятую вместо точки
    'username@',  # Отсутствует доменное имя
    'username@domain@domain.com',  # Содержит два символа @
    'username@domain..domain.com',  # Содержит два точечных символа
    # FIXME: domain.-com - дает ложно отрицательный результат в тесте
    # 'username@domain.-com',  # Домен начинается с недопустимого символа
]


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
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(email='')
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.parametrize('bad_email', invalid_emails)
@pytest.mark.django_db()
def test_bad_format_email_required_field(
    bad_email: str,
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test to check with different non-valid email formats."""
    user_with_invalid_email = registration_data_factory(email=bad_email)
    response = client.post(
        reverse('identity:registration'),
        data=user_with_invalid_email,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=user_with_invalid_email['email'])


@pytest.mark.django_db()
def test_user_manager_create_error(random_string):
    """If email is missing, error is called."""
    random_user = {
        'email': None,
        'password': random_string(),
        'first_name': random_string(),
        'last_name': random_string(),
        'phone': random_string(),
    }
    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(**random_user)

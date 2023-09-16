import datetime
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_login_page(client: Client) -> None:
    """Test ensures that login page is accessible."""
    response = client.get('/identity/login')

    assert response.status_code == HTTPStatus.OK


def test_logout_page(client: Client) -> None:
    """Test ensures that logout page is accessible and redirects to index."""
    response = client.get('/identity/logout')

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('index')


@pytest.mark.django_db()
def test_registration_page(client: Client) -> None:
    """The test ensures that registration is valid."""
    registration_data = {
        'email': 'test@example.com',
        'last_name': 'Тестов',
        'first_name': 'Тест',
        'date_of_birth': '2023-01-01',
        'address': 'РФ',
        'job_title': 'Тестировщик',
        'phone': '+79000000000',
        'password1': '12345678',
        'password2': '12345678',
    }

    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')

    user = User.objects.get(email=registration_data['email'])
    assert user.first_name == registration_data['first_name']
    assert user.last_name == registration_data['last_name']
    assert user.date_of_birth == datetime.datetime.strptime(
        registration_data['date_of_birth'], '%Y-%m-%d',
    ).date()
    assert user.address == registration_data['address']
    assert user.job_title == registration_data['job_title']
    assert user.phone == registration_data['phone']
    assert user.is_active
    assert not user.is_superuser
    assert not user.is_staff


def test_update_user_details_page(client: Client) -> None:
    """Test ensures that update page is accessible."""
    response = client.get('/identity/update')

    assert response.status_code == HTTPStatus.FOUND

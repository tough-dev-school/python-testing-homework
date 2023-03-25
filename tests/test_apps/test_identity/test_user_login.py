from http import HTTPStatus

import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse
from mimesis.locales import Locale
from mimesis.schema import Field

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_valid_user_login(register_user: dict[str, str], client: Client):

    response = client.post(
        reverse('identity:login'),
        data=register_user
    )
    user = auth.get_user(client)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('location') == reverse('pictures:dashboard')
    assert user.is_authenticated


@pytest.mark.django_db()
def test_wrong_username_not_logged(register_user: dict[str, str], client: Client, faker_seed: int):
    mf = Field(locale=Locale.RU, seed=faker_seed+1)
    email = mf('person.email')

    response = client.post(
        reverse('identity:login'),
        data={'username': email, 'password': register_user['password']}
    )
    user = auth.get_user(client)

    assert not User.objects.filter(email=email)
    assert not user.is_authenticated
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_wrong_password_not_logged(register_user: dict[str, str], client: Client, faker_seed: int):
    mf = Field(locale=Locale.RU, seed=faker_seed+1)
    password = mf('password')

    response = client.post(
        reverse('identity:login'),
        data={'username': register_user['username'], 'password': password}
    )
    user = auth.get_user(client)

    assert User.objects.filter(email=register_user['username'])
    assert not user.is_authenticated
    assert response.status_code == HTTPStatus.OK
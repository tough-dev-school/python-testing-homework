import random
from http import HTTPStatus
from typing import TYPE_CHECKING, List

import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse
from mimesis.locales import Locale
from mimesis.schema import Field

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import LoginData


@pytest.mark.django_db()
def test_valid_user_login(register_user: "LoginData", client: Client):

    response = client.post(
        reverse('identity:login'),
        data=register_user
    )
    user = auth.get_user(client)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('location') == reverse('pictures:dashboard')
    assert user.is_authenticated


seed = random.Random().getrandbits(32)

def get_invalid_logins(faker_seed: int) -> List[str]:
    invalid_logins = [''] # start with empty login

    mf = Field(locale=Locale.RU, seed=faker_seed+1)
    for _ in range(5):
        invalid_logins.append(mf('person.email'))

    return invalid_logins


def get_invalid_passwords(faker_seed: int) -> List[str]:
    invalid_passwords = [''] # start with empty password

    mf = Field(locale=Locale.RU, seed=faker_seed+1)
    for _ in range(5):
        invalid_passwords.append(mf('password'))

    return invalid_passwords


@pytest.mark.django_db()
@pytest.mark.parametrize('username', get_invalid_logins(seed))
@pytest.mark.parametrize('password', get_invalid_passwords(seed))
def test_bad_field_no_login(username: str, password: str, register_user: "LoginData", client: Client):

    response = client.post(
        reverse('identity:login'),
        data={'username': username, 'password': password}
    )
    user = auth.get_user(client)

    assert User.objects.filter(email=register_user['username'])
    assert not user.is_authenticated
    assert response.status_code == HTTPStatus.OK

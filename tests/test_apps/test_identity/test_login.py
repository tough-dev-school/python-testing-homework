from http import HTTPStatus

import pytest

from server.apps.identity.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_login_user_positive(client, register_user_factory):
    user_email, user_pass = register_user_factory()
    response = client.post(
        reverse("identity:login"),
        data={
            "username": user_email,
            "password": user_pass
        }
    )
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_login_user_negative(client, register_user_factory):
    user_email, _ = register_user_factory()
    response = client.post(
        reverse("identity:login"),
        data={
            "username": user_email,
            "password": "some_invalid_pass"
        }
    )
    assert response.status_code == HTTPStatus.OK

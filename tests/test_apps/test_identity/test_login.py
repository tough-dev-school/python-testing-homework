from http import HTTPStatus

import pytest

from server.apps.identity.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_login_user_valid(client, register_user_factory):
    user = register_user_factory()
    # user_data = User.objects.filter(email=user["email"])
    response = client.post(
        reverse("identity:login"),
        data={
            "username": user["email"],
            "password": user["password"]
        }
    )
    assert response.status_code == HTTPStatus.FOUND

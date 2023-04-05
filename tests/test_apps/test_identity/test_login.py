from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_login_user_positive(
    client: Client, create_new_user_factory: "CreateUserFactory"
) -> None:
    user_info = create_new_user_factory()
    response = client.post(
        reverse("identity:login"),
        data={
            "username": user_info["email"],
            "password": user_info["password"],
        },
    )
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_login_user_negative(
    client, create_new_user_factory: "CreateUserFactory"
) -> None:
    user_info = create_new_user_factory()
    response = client.post(
        reverse("identity:login"),
        data={"username": user_info["email"], "password": "some_invalid_pass"},
    )
    assert response.status_code == HTTPStatus.OK

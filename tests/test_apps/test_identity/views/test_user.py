from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from factory.base import FactoryMetaClass

from server.apps.identity.models import User

pytestmark = pytest.mark.django_db


def test_unauthorized_user_update(client: Client) -> None:
    response = client.get(reverse("identity:user_update"))

    assert response.status_code == HTTPStatus.FOUND
    assert response.get("Location", "") == "/identity/login?next=/identity/update"


def test_user_update_page_renders(authenticated_client: Client) -> None:
    response = authenticated_client.get(reverse("identity:user_update"))

    assert response.status_code == HTTPStatus.OK
    assert response.get("Content-Type") == "text/html; charset=utf-8"


def test_valid_user_update(
    authenticated_client: Client,
    user: User,
    user_update_data_factory: FactoryMetaClass,
    assert_correct_user,
) -> None:
    updated_data = user_update_data_factory()

    response = authenticated_client.post(reverse("identity:user_update"), updated_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.get("Location", "") == reverse("identity:user_update")
    assert_correct_user(user.email, updated_data)

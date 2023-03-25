from http import HTTPStatus
from typing import Dict

import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse
from django.utils.crypto import get_random_string


@pytest.mark.django_db()
def test_login_valid(signup_user: Dict[str, str], client: Client):
    """Test a registred user can login."""
    response = client.post(reverse("identity:login"), data=signup_user)
    user = auth.get_user(client)

    assert response.status_code == HTTPStatus.FOUND
    assert user.is_authenticated
    assert response.get("location") == reverse("pictures:dashboard")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ("invalid_field", "invalid_value"),
    [
        ("username", f"{get_random_string(5)}@email.com"),
        ("password", get_random_string(10)),
    ],
)
def test_login_invalid(
    signup_user: Dict[str, str],
    client: Client,
    invalid_field: str,
    invalid_value: str,
):
    """Test a unregistred user and a user with wring password can not login."""
    post_data = signup_user | {
        invalid_field: invalid_value,  # type: ignore[arg-type]
    }

    response = client.post(reverse("identity:login"), data=post_data)
    user = auth.get_user(client)

    assert response.status_code == HTTPStatus.OK
    assert not user.is_authenticated

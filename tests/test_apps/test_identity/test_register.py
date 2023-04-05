from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from tests.plugins.assertions.user import UserAssertion, UserAssertionNegative
from tests.plugins.identity.user import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: "RegistrationData",
    user_data: "UserData",
    assert_correct_user: "UserAssertion",
) -> None:
    response = client.post(
        reverse("identity:registration"),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get("Location") == reverse("identity:login")
    assert_correct_user(registration_data["email"], user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize("field", User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: "RegistrationDataFactory",
    field: str,
    assert_user_not_registered: "UserAssertionNegative",
) -> None:
    user_data = registration_data_factory(**{field: ""})
    response = client.post(reverse("identity:registration"), data=user_data)
    assert_user_not_registered(response.status_code, user_data["email"])


@pytest.mark.django_db()
def test_invalid_password_confirmation(
    client: Client,
    registration_data: "RegistrationData",
    assert_user_not_registered: "UserAssertionNegative",
):
    user_data = registration_data
    user_data["password1"] = "some_pass"
    user_data["password2"] = "invalid_pass"
    response = client.post(reverse("identity:registration"), data=user_data)
    assert_user_not_registered(response.status_code, user_data["email"])

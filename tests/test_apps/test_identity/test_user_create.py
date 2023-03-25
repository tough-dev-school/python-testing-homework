from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


@pytest.fixture(scope="session")
def assert_correct_user() -> "UserAssertion":
    def factory(email: str, expected: "UserData") -> None:
        user = User.objects.get(email=email)

        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory


# test user can be created with valid data
@pytest.mark.django_db()
def test_create_user_with_valid_data(
    client: Client,
    registration_data: "RegistrationData",
    expected_user_data: "UserData",
    assert_correct_user: "UserAssertion",
) -> None:
    response = client.post(
        reverse("identity:registration"),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get("location") == reverse("identity:login")
    assert_correct_user(registration_data["email"], expected_user_data)


# test user can not be created with any empty field
@pytest.mark.django_db()
@pytest.mark.parametrize("field", User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_create_user_empty_field(
    client: Client,
    registration_data_factory: "RegistrationDataFactory",
    field: str,
) -> None:
    post_data = registration_data_factory(
        **{field: ""},
    )

    response = client.post(reverse("identity:registration"), data=post_data)

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data["email"])

@pytest.mark.django_db()
def test_create_user_no_email(
    client: Client,
    registration_data_factory: "RegistrationDataFactory",
) -> None:
    post_data = registration_data_factory()
    post_data.pop('email')

    with pytest.raises(TypeError):
        User.objects.create_user(**post_data)


        #assert response.status_code == HTTPStatus.OK
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data_factory,
    expected_user_data
) -> None:
    response = client.post(
        reverse("identity:registration"),
        data={
            "email": "some_email@email.ru",
            "first_name": "some_name"
        }
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get("Location") == reverse("identity:login")
    assert_correct_user(registration_data_factory["email"], expected_user_data)


@pytest.mark.django_db
@pytest.mark.parametrize("field", User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client,
    registration_data_factory,
    field
):
    user_data = registration_data_factory(
        **{field: ""}
    )
    response = client.post(
        reverse("identity:registration"),
        data=user_data
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=user_data["email"])

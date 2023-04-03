from http import HTTPStatus

import pytest

from server.apps.identity.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_user_data_updated(
    client, signup_user, registration_data_factory, user_data, assert_correct_user
):
    user_info = signup_user
    update_user_data = registration_data_factory(email=user_info["email"])
    response = client.post(reverse("identity:user_update"), data=update_user_data)

    assert response.status_code == HTTPStatus.FOUND
    assert_correct_user(user_info["email"], user_data)

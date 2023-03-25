from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_happy_path(
    registration_user_data,
    client: Client,
    assert_correct_user,
):
    """Test checks that UseCase "create new user" works with right data."""
    resp = client.post(
        reverse('identity:registration'),
        data=registration_user_data,
    )
    assert resp.status_code == HTTPStatus.FOUND
    assert_correct_user(
        email=registration_user_data['email'],
        expected=registration_user_data,
    )


@pytest.mark.django_db()
def test_empty_email(
    registration_user_data,
    client: Client,
    assert_correct_user,
):
    """Test checks UserModel can't create instance with empty email field."""
    with pytest.raises(ValueError):  # noqa: PT011
        User.objects.create_user(
            email='',
            password=registration_user_data['password'],
        )

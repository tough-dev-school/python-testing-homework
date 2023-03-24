from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_signup(
    client: Client,
    user_credentials,
    user_data,
    assert_user_was_created,
):
    """Test user registration."""
    response = client.post(
        reverse('identity:registration'),
        data={**user_credentials, **user_data},
    )

    assert response.status_code == HTTPStatus.FOUND
    assert_user_was_created(user_credentials, user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_missing_required_fields(
    client: Client,
    user_credentials,
    user_data,
    assert_user_was_created,
    field: str,
):
    """Test user registration with missing required fields."""
    response = client.post(
        reverse('identity:registration'),
        data={
            **user_credentials,
            **user_data,
            **{field: ''},
        },
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_user_already_exists(
    client: Client,
    user: User,
    user_credentials,
    user_data,
):
    """Test user registration with already existing user."""
    response = client.post(
        reverse('identity:registration'),
        data={
            **user_credentials,
            **user_data,
            **{User.USERNAME_FIELD: user.email},
        },
    )
    assert response.context['form'].errors
    assert response.status_code == HTTPStatus.OK

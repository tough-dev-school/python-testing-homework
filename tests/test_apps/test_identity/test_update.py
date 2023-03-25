from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_valid_update(
    client: Client,
    user,
    user_data,
    assert_user_update,
    external_api_mock_update
):
    """Test user update."""
    client.force_login(user)
    response = client.post(
        reverse('identity:user_update'),
        data=user_data,
    )
    print(user_data)
    assert response.status_code == HTTPStatus.FOUND
    assert_user_update(user, user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS)
def test_invalid_update(
    client: Client,
    user,
    user_data,
    field: str,

):
    """Test user update with invalid data."""
    client.force_login(user)
    response = client.post(
        reverse('identity:user_update'),
        data={
            **user_data,
            **{field: ''},
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.context['form'].errors

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_valid_update(
    client: Client,
    user,
    user_data,
    assert_user_update,
):
    """Test user update."""
    client.force_login(user)
    response = client.post(
        reverse('identity:user_update'),
        data=user_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert_user_update(user, user_data)

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from protocols.identity.user import UserDict
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_update_endpoint_happy_path(
    authed_user_data: User,
    update_user_data: UserDict,
    client: Client,
    assert_correct_update_user,
):
    """Test checks user update endpoint on correct data."""
    client.force_login(user=authed_user_data)
    resp = client.post(
        reverse('identity:user_update'), update_user_data, follow=True,
    )
    assert resp.status_code == HTTPStatus.OK

    assert_correct_update_user(
        user_before=authed_user_data, expected=update_user_data,
    )

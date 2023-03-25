from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_login_happy_path(
    client: Client,
    authed_user_data,
    login_data,
):
    """Test checks that login works with right data input."""
    resp = client.post(reverse('identity:login'), login_data)

    assert resp.status_code == HTTPStatus.FOUND

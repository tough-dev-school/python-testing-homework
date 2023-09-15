from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db()()
def test_login(client: Client) -> None:
    """This test ensures that health check is accessible."""
    response = client.get('/identity/login')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_admin_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel is accessible."""
    response = admin_client.get('/identity/logout/')

    assert response.status_code == HTTPStatus.OK

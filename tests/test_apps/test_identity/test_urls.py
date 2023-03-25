from http import HTTPStatus

import pytest
from django.test import Client


def test_login_unauthorized(client: Client) -> None:
    """This test ensures that identity is accessible."""
    response = client.get('/identity/login')

    assert response.status_code == HTTPStatus.OK
    assert b'docutils' not in response.content


def test_registration_authorized(client: Client) -> None:
    """This test ensures that identity is accessible."""
    response = client.get('/identity/registration')

    assert response.status_code == HTTPStatus.OK
    assert b'user-model-form' in response.content

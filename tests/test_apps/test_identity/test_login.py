from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_login_as_user(client: Client, user: User, mock_authenticate):
    """Login as user."""
    response = client.post(
        reverse('identity:login'),
        data={
            'username': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_login_as_non_existing_user(client: Client, mock_authenticate):
    """Login as non-existing user."""
    response = client.post(
        reverse('identity:login'),
        data={
            'username': 'non-existing',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.context['form'].errors

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    create_user: User,
) -> None:
    """A valid user login must redirect to the home page."""
    client.force_login(create_user)

    response = client.get(reverse('index'))

    assert response.status_code == HTTPStatus.OK
    assert 'Личный кабинет'.encode('utf-8') in response.content

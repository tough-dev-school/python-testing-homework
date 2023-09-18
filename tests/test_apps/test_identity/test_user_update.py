from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_update_template(
    client: 'Client',
    create_user: 'User',
) -> None:
    """Test get template for update user."""
    client.force_login(create_user)
    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
    assert 'Редактировать профиль'.encode('utf-8') in response.content

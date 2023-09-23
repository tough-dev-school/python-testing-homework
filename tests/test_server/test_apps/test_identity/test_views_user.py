from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

pytestmark = pytest.mark.django_db


def test_user_update_view(
    authorized_client: 'Client',
) -> None:
    """Test update auth user view."""
    response = authorized_client.get(reverse('identity:user_update'))
    assert response.status_code == HTTPStatus.OK
    assert response.template_name.__contains__('identity/pages/user_update.html')


def test_non_auth_user_update_view(client: 'Client'):
    response = client.post(reverse('identity:user_update'), data={})
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location').startswith(reverse('identity:login'))


def test_non_auth_user_registration_view(client: 'Client') -> None:
    response = client.get(reverse('identity:login'))
    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type').startswith('text/html')


def test_auth_user_registration_view(authorized_client: 'Client') -> None:
    response = authorized_client.get(reverse('identity:login'))
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')

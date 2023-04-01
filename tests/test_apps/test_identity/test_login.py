from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.settings.components.identity import LOGIN_REDIRECT_URL

if TYPE_CHECKING:
    from tests.plugins.identity.user import LoginData, LoginDataFactory


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    login_data: 'LoginData',
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that login works with correct login data."""
    with monkeypatch.context() as patch:
        patch.setattr(User, 'check_password', lambda *args: True)
        response = client.post(
            reverse('identity:login'),
            data=login_data,
        )
    assert response.status_code == HTTPStatus.FOUND

    response.url.startswith(str(LOGIN_REDIRECT_URL))
    response = client.get(response.url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_with_no_existing_user(
    client: Client,
    login_data_factory: 'LoginDataFactory',
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that login works with no existing user."""
    post_data = login_data_factory(**{'username': 'no_such_user@test.com'})
    with monkeypatch.context() as patch:
        patch.setattr(User, 'check_password', lambda *args: True)
        response = client.post(
            reverse('identity:login'),
            data=post_data,
        )
    assert response.context['form'].errors
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@pytest.mark.parametrize('field', ['username', 'password'])
def test_login_missing_required_field(
    client: Client,
    login_data_factory: 'LoginDataFactory',
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    """Test that login works with missing required fields."""
    post_data = login_data_factory(**{field: ''})
    with monkeypatch.context() as patch:
        patch.setattr(User, 'check_password', lambda *args: True)
        response = client.post(
            reverse('identity:login'),
            data=post_data,
        )
    assert response.context['form'].errors
    assert response.status_code == HTTPStatus.OK

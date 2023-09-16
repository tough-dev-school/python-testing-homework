from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from .conftest import RegistrationData, UserAssertion, LoginData


@pytest.mark.django_db()
@pytest.mark.parametrize('page', ['/identity/login', '/identity/registration'])
def test_identity_pages_unauthenticated(client: Client, page: str) -> None:
    """test accessibility of identity pages for unauthenticated users"""

    response = client.get(page)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@pytest.mark.parametrize('page', ['/pictures/dashboard', '/pictures/favourites'])
def test_pictures_pages_unauthenticated(client: Client, page: str) -> None:
    """test ensures that unauthenticated users are redirected to login page"""

    response = client.get(page)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/identity/login?next=' + page


@pytest.mark.django_db()
def test_valid_registration(
        client: Client,
        registration_data: RegistrationData,
        assert_correct_user: UserAssertion,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data)


@pytest.mark.django_db()
def test_user_login(
        client: Client,
        create_new_user: User,
        login_data: LoginData,
) -> None:
    """Check user login."""
    response = client.post(
        reverse('identity:login'),
        data=login_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')
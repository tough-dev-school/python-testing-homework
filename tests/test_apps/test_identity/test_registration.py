from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db

from tests.plugins.identity.user import RegistrationData, UserDataExtractor, UserAssertion


@pytest.mark.parametrize('page', ['/identity/login', '/identity/registration'])
def test_identity_pages_unauthenticated(client: Client, page: str) -> None:
    """test accessibility of identity pages for unauthenticated users"""

    response = client.get(page)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('page', ['/pictures/dashboard', '/pictures/favourites'])
def test_pictures_pages_unauthenticated(client: Client, page: str) -> None:
    """test ensures that unauthenticated users are redirected to login page"""

    response = client.get(page)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/identity/login?next=' + page


def test_valid_registration(
        client: Client,
        registration_data: RegistrationData,
        user_data: UserDataExtractor,
        assert_correct_user: UserAssertion,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(
        registration_data['email'],
        user_data(registration_data),
    )

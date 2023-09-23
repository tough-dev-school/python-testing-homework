from http import HTTPStatus

import pytest
from django.test import Client
from plugins.identity.user import (
    ProfileAssertion,
    ProfileDataFactory,
    logged_user_client
)


@pytest.mark.django_db()()
def test_health_check(client: Client) -> None:
    """This test ensures that health check is accessible."""
    response = client.get('/health/')

    assert response.status_code == HTTPStatus.OK


def test_admin_unauthorized(client: Client) -> None:
    """This test ensures that admin panel requires auth."""
    response = client.get('/admin/')

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_admin_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel is accessible."""
    response = admin_client.get('/admin/')

    assert response.status_code == HTTPStatus.OK


def test_admin_docs_unauthorized(client: Client) -> None:
    """This test ensures that admin panel docs requires auth."""
    response = client.get('/admin/doc/')

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_admin_docs_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel docs are accessible."""
    response = admin_client.get('/admin/doc/')

    assert response.status_code == HTTPStatus.OK
    assert b'docutils' not in response.content


@pytest.mark.parametrize("url_found", [
    '/pictures/dashboard',
    '/pictures/favourites'
])
def test_picture_pages_unauthorized(client: Client, url_found: str) -> None:
    """This test ensures that picture management pages require auth."""
    response = client.get(url_found)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
@pytest.mark.parametrize("url_accessible", [
    '/pictures/dashboard',
    '/pictures/favourites'
])
def test_picture_pages_authorized(
    logged_user_client: Client,
    url_accessible: str
) -> None:
    """Ensures picture management pages are accessible for authorized user."""

    response = logged_user_client.get(url_accessible)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_profile_update_authorized(
    logged_user_client: Client,
    profile_data_factory: 'ProfileDataFactory',
    assert_correct_profile: 'ProfileAssertion',
    assert_incorrect_profile: 'ProfileAssertion',
) -> None:
    """This test ensures profile updating for an authorized user."""
    user_data = profile_data_factory()

    # that is an email for `logged_user_client` fixture
    # maybe add indirect parametrization?
    email = 'email@example.com'

    # there might be a probability of accidental match, but disregard it for now
    assert_incorrect_profile(email, user_data)

    response = logged_user_client.post(
        '/identity/update',
        data=user_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == '/identity/update'
    assert_correct_profile(email, user_data)


@pytest.mark.parametrize('page', [
    '/robots.txt',
    '/humans.txt',
])
def test_specials_txt(client: Client, page: str) -> None:
    """This test ensures that special `txt` files are accessible."""
    response = client.get(page)

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/plain'

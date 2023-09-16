from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.test import Client
from plugins.identity.user import ProfileAssertion, ProfileDataFactory


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


def test_picture_pages_unauthorized(client: Client) -> None:
    """This test ensures that picture management pages require auth."""
    response = client.get('/pictures/dashboard')
    assert response.status_code == HTTPStatus.FOUND

    response = client.get('/pictures/favourites')
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_picture_pages_authorized(
    client: Client,
    django_user_model: User,
) -> None:
    """Ensures picture management pages are accessible for authorized user."""
    password, email = 'password', 'email@example.com'
    user = django_user_model.objects.create_user(
        email,
        password,
    )
    client.force_login(user)

    response = client.get('/pictures/dashboard')
    assert response.status_code == HTTPStatus.OK

    response = client.get('/pictures/favourites')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_profile_update_authorized(
    client: Client,
    django_user_model: User,
    profile_data_factory: 'ProfileDataFactory',
    assert_correct_profile: 'ProfileAssertion',
    assert_incorrect_profile: 'ProfileAssertion',
) -> None:
    """This test ensures profile updating for an authorized user."""
    user_data = profile_data_factory()

    password, email = 'password', 'email@example.com'
    user = django_user_model.objects.create_user(
        email,
        password,
    )
    client.force_login(user)

    # there might be a probability of accidental match, but disregard it for now
    assert_incorrect_profile(email, user_data)

    response = client.post(
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

from http import HTTPStatus

import pytest
from django.test import Client


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
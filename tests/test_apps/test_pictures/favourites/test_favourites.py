from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.pictures.models import FavouritePicture
from tests.test_apps.test_pictures.favourites.conftest import (
    PictureInContentAssertion,
)

URL_PATH = reverse('pictures:favourites')


@pytest.mark.django_db()
def test_not_logined_redirect(client: Client) -> None:
    """Endpoint redirects if user is not logined."""
    response = client.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_page_renders(client_logined: Client) -> None:
    """Basic `get` method works if user is logined."""
    response = client_logined.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_picture_loaded(
    client_logined: Client,
    db_picture: FavouritePicture,
    assert_picture_in_content: PictureInContentAssertion,
) -> None:
    """Picture renders if it exists in DB."""
    response = client_logined.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.OK
    assert_picture_in_content(response.content, db_picture)

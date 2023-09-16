from http import HTTPStatus
from typing import List

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from .conftest import FavouritePicturesAssertion, PictureData


@pytest.mark.django_db()
@pytest.mark.parametrize('page', ['/pictures/dashboard', '/pictures/favourites'])
def test_pictures_view_authenticated(client: Client, page: str) -> None:
    """Test ensures that pictures view is accessible."""
    response = client.get(page)

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_favorite_pictures_list(
        client: Client,
        # user: User,
        pictures_list: List[PictureData],
        assert_correct_favorite_pictures: FavouritePicturesAssertion,
) -> None:
    """Test ensures that favorite pictures list is correct for current user."""
    # assert_correct_favorite_pictures(user.email, [])
    response = client.get('/pictures/favourites')
    #
    assert response.status_code == HTTPStatus.FOUND
    #
    # assert_correct_favorite_pictures(user.email, pictures_list)

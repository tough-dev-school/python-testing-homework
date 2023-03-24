from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test__fetch_one(user: User, one_user_favourite: FavouritePicture) -> None:
    """Test getting favourite."""
    fav_items = FavouritesList()(user.id).all()

    assert len(fav_items) == 1
    assert fav_items[0].id == one_user_favourite.id


@pytest.mark.django_db()
def test_non_auth_redirect(client: Client) -> None:
    """Test getting non-authentificated redirect."""
    response = client.post(reverse('pictures:dashboard'), data={})

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/identity/login?next=/pictures/dashboard'


@pytest.mark.django_db()
def test_sign_user_add_one_favourite(
    client: Client,
    signedin_user: User,
    favourite_picture_data: 'FavouritePictureData',
) -> None:
    """Test signed user add favourite."""
    response = client.post(
        reverse('pictures:dashboard'),
        data=favourite_picture_data.dict(),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')
    fav_items = FavouritesList()(signedin_user.id).all()
    assert len(fav_items) == 1
    assert fav_items[0].foreign_id == favourite_picture_data.foreign_id
    assert fav_items[0].url == favourite_picture_data.url

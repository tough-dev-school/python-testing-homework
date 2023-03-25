from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_fetch_zero_favourites(signedin_user: User) -> None:
    """Test getting zero favourites."""
    fav_items = FavouritesList()(signedin_user.id).all()

    assert not fav_items


@pytest.mark.django_db()
def test_fetch_one_favourite(
    signedin_user: User,
    one_user_favourite: FavouritePicture,
) -> None:
    """Test getting one favourite."""
    fav_items = FavouritesList()(signedin_user.id).all()

    assert len(fav_items) == 1
    assert fav_items[0].id == one_user_favourite.id


@pytest.mark.django_db()
def test_non_auth_redirect(client: Client) -> None:
    """Test getting non-authentificated redirect."""
    response = client.post(reverse('pictures:dashboard'), data={})

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/identity/login?next=/pictures/dashboard'


@pytest.mark.django_db()
def test_sign_user_post_one_favourite(
    client: Client,
    signedin_user: User,
    favourite_picture_data: 'FavouritePictureData',  # noqa: F821
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


@pytest.mark.django_db()
def test_sign_user_post_two_same_favourites(
    client: Client,
    signedin_user: User,
    favourite_picture_data: 'FavouritePictureData',  # noqa: F821
) -> None:
    """Test signed user add two same favourites."""
    dashboard_url = reverse('pictures:dashboard')
    favourite_picture_dict = favourite_picture_data.dict()
    response = client.post(
        dashboard_url,
        data=favourite_picture_dict,
    )
    response = client.post(
        dashboard_url,
        data=favourite_picture_dict,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')
    fav_items = FavouritesList()(signedin_user.id).all()
    assert len(fav_items) == 2
    assert fav_items[0].foreign_id == favourite_picture_data.foreign_id
    assert fav_items[0].url == favourite_picture_data.url
    assert fav_items[1].foreign_id == favourite_picture_data.foreign_id
    assert fav_items[1].url == favourite_picture_data.url


@pytest.mark.django_db()
def test_sign_user_post_multiply_favourites(
    client: Client,
    signedin_user: User,
    favourite_picture_data: 'FavouritePictureData',  # noqa: F821
) -> None:
    """Test signed user add many favourite."""
    count = 10
    for _ in range(count):
        response = client.post(
            reverse('pictures:dashboard'),
            data=favourite_picture_data.dict(),
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('pictures:dashboard')

    fav_pictures = FavouritesList()(signedin_user.id).all()
    assert len(fav_pictures) == count
    for picture in fav_pictures:
        assert picture.foreign_id == favourite_picture_data.foreign_id
        assert picture.url == favourite_picture_data.url

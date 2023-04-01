from http import HTTPStatus

import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse
from mimesis import Field
from plugins.pictures.picture import FavouritePictureData

from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture


@pytest.fixture()
def favourite_picture(mf: Field) -> FavouritePictureData:

    return FavouritePictureData(  # type: ignore
        foreign_id=mf('numeric.increment'),
        url=mf('internet.uri'),
    )


@pytest.mark.django_db()
def test_add_favourite_picture(logged_client: Client,
                               favourite_picture: "FavouritePictureData"):
    response = logged_client.post(
        reverse("pictures:dashboard"),
        data=favourite_picture)

    assert response.status_code == HTTPStatus.FOUND

    user = auth.get_user(logged_client)
    fav_pics = FavouritesList()(user.id)
    assert len(fav_pics) == 1

    assert fav_pics[0].foreign_id == favourite_picture['foreign_id']
    assert fav_pics[0].url == favourite_picture['url']

@pytest.mark.django_db()
def test_picture_has_str(
    favourite_picture: "FavouritePictureData",
    logged_client: Client):
    user = auth.get_user(logged_client)
    fav_pic = FavouritePicture(
        foreign_id=favourite_picture['foreign_id'],
        url=favourite_picture['url'],
        user=user,
    )

    assert str(fav_pic) == '<Picture {0} by {1}>'.format(favourite_picture['foreign_id'], user.id)

from http import HTTPStatus

import pytest
from django.urls import reverse

from server.apps.pictures.logic.usecases.favourites_list import FavouritesList


@pytest.mark.django_db()
def test_add_favourite_picture(
    get_user_object, add_favourite_picture, valid_new_picture, signup_user
):
    user = get_user_object(signup_user["email"])
    picture = valid_new_picture
    add_favourite_picture(picture)
    user_favourite = FavouritesList()(user.id).first()
    assert user_favourite.foreign_id == picture["foreign_id"]


@pytest.mark.django_db()
def test_add_favourite_picture_invalid_fields(
    client, picture_data_factory, signup_user
):
    picture = picture_data_factory(foreign_id="some_invalid_val")
    response = client.post(reverse("pictures:dashboard"), data=picture)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_get_dashboard(client, signup_user):
    response = client.get(reverse("pictures:dashboard"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_add_favourite_noauth(client, picture_data_factory):
    picture = picture_data_factory()
    response = client.post(reverse("pictures:dashboard"), data=picture)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/identity/login?next=/pictures/dashboard"


@pytest.mark.django_db()
def test_add_favourite_same_picture(
    get_user_object, add_favourite_picture, signup_user, picture_data_factory
):
    user = get_user_object(signup_user["email"])
    picture = picture_data_factory()
    for _ in range(2):
        add_favourite_picture(picture)
    user_favourite = FavouritesList()(user.id).all()
    assert all(
        [picture["foreign_id"] == fav_pic.foreign_id for fav_pic in user_favourite]
    )
    assert all([picture["url"] == fav_pic.url for fav_pic in user_favourite])

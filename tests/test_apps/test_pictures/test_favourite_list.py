from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from django_fakery import factory

from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_favourite_list(
    client: Client,
    authed_user_data,
):
    """Test checks that logged-in user have access to pictures."""
    client.force_login(authed_user_data)
    resp = client.get(reverse('pictures:favourites'))
    assert resp.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_picture_message(
    db_user,
):
    """Test checks the __str__ method of FavouritePicture works right."""
    pic: FavouritePicture = factory.m(FavouritePicture)(
        user=db_user, url='http://0.0.0.0:5001', foreign_id=1,
    )
    assert str(pic) == '<Picture {0} by {1}>'.format(1, db_user.id)

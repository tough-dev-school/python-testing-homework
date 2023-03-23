from http import HTTPStatus
import pytest
from django.test import Client
from django.urls import reverse
from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db
def test_one_favourite(user: User, one_user_favourite: FavouritePicture) -> None:
    """Test getting favourite."""
    items = FavouritesList()(user.id).all()

    assert len(items) == 1
    assert items[0].id == one_user_favourite.id


@pytest.mark.django_db
def test_non_auth_redirect(client: Client) -> None:
    """Test getting non-authentificated redirect."""
    response = client.post(reverse('pictures:dashboard'), data={})

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == '/identity/login?next=/pictures/dashboard'

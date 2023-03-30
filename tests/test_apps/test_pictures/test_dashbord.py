from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:
    from tests.plugins.identity.user import UserData
    from tests.plugins.pictures.picture import PictureData


@pytest.mark.django_db()
def test_valid_dashboard_with_1_favourite(
    client: Client,
    db_user: 'UserData',
    picture_data: 'PictureData',
) -> None:
    """Test correct picture adding."""
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)

    response = client.post(
        reverse('pictures:dashboard'),
        data=picture_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert FavouritePicture.objects.get(user=user)
    assert response.url == reverse('pictures:dashboard')


@pytest.mark.django_db()
def test_valid_dashboard_with_2_favourites(
    client: Client,
    db_user: 'UserData',
    picture_data: 'PictureData',
) -> None:
    """Test correct two pictures adding."""
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)

    dashboard_url = reverse('pictures:dashboard')
    response = client.post(
        dashboard_url,
        data=picture_data,
    )
    response = client.post(
        dashboard_url,
        data=picture_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    db_pictures = FavouritePicture.objects.filter(user=user).all()
    assert len(db_pictures) == 2
    assert db_pictures[0].foreign_id == picture_data["foreign_id"]
    assert db_pictures[0].url == picture_data["url"]
    assert db_pictures[1].foreign_id == picture_data["foreign_id"]
    assert db_pictures[1].url == picture_data["url"]
    assert response.url == reverse('pictures:dashboard')


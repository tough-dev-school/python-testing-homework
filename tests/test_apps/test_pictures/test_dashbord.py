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
def test_valid_dashboard(
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

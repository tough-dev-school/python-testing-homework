from http import HTTPStatus
from typing import TYPE_CHECKING, Tuple

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:  # noqa: WPS604
    from tests.plugins.identity.user import UserData
    from tests.plugins.pictures.pictures import PictureData


@pytest.mark.django_db()
def test_favourite(
    client: Client,
    user_registration: Tuple['UserData', HttpResponse],
    picture_data: 'PictureData',
) -> None:
    """Test correct picture adding."""
    user_data, user_resp = user_registration
    user = User.objects.get(email=user_data['email'])
    client.force_login(user)

    response = client.post(
        reverse('pictures:dashboard'),
        data=picture_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert FavouritePicture.objects.get(user=user) is not None

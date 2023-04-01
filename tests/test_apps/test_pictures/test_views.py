from http import HTTPStatus
from typing import TYPE_CHECKING, Callable, Any  # noqa: I001

import httpretty
import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from tests.plugins.constants import LIMIT_EXTERNAL_ITEMS_FINAL

if TYPE_CHECKING:  # noqa: WPS604
    from tests.plugins.pictures.pictures import PictureData


@pytest.mark.django_db()
def test_favourite_create(
    client: Client,
    user_registration: User,
    picture_data: 'PictureData',
) -> None:
    """Test correct picture adding."""
    user = user_registration

    response = client.post(
        reverse('pictures:dashboard'),
        data=picture_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert FavouritePicture.objects.get(user=user) is not None


@pytest.mark.django_db()
def test_favourite_view(
    client: Client,
    picture_creation: FavouritePicture,
) -> None:
    """Test correct picture adding."""
    response = client.get(
        reverse('pictures:favourites'),
    )
    actual_picture_favorite = response.context['object_list'][0]

    assert response.status_code == HTTPStatus.OK
    assert actual_picture_favorite == picture_creation


@pytest.mark.django_db()
@httpretty.activate  # type: ignore[misc]
def test_placeholder_external_service(
    client: Client,
    mock_pictures_service: Callable[[Any], None],
    picture_data: 'PictureData',
    user_registration: User,
) -> None:
    """Test pictures placeholder."""
    pictures = [{
        'id': picture_data.get('foreign_id'),
        'url': picture_data.get('url'),
    }]
    mock_pictures_service(pictures)

    response = client.get(
        reverse('pictures:dashboard'),
    )

    assert response.status_code == HTTPStatus.OK
    assert pictures[0]['id'] == response.context['pictures'][0].id


@pytest.mark.django_db()
@pytest.mark.timeout(4)
@pytest.mark.usefixtures('_apply_json_server')
def test_external_service(
    client: Client,
    picture_data: 'PictureData',
    user_registration: User,
) -> None:
    """Test pictures placeholder with json-server."""
    response = client.get(
        reverse('pictures:dashboard'),
    )
    response_pictures = response.context['pictures']

    assert LIMIT_EXTERNAL_ITEMS_FINAL == len(response_pictures)

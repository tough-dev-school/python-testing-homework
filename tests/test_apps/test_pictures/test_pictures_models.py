"""Test pictures models."""
from typing import Any

import pytest
from mimesis import Generic, Internet

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture

pytestmark = pytest.mark.django_db

generic = Generic()
internet = Internet()
MIN_FOREIGN_ID = 10000
MAX_FOREIGN_ID = 99999
FOREIGN_ID = generic.random.randint(MIN_FOREIGN_ID, MAX_FOREIGN_ID)
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
URL = str(internet.stock_image(width=IMAGE_WIDTH, height=IMAGE_HEIGHT))


def test_fav_picture_model(user_data: dict[str, Any]) -> None:
    """Test FavouritePicture model creation."""
    user = User.objects.create_user(**user_data)

    fav_picture = FavouritePicture.objects.create(
        user=user,
        foreign_id=FOREIGN_ID,
        url=URL,
    )

    assert fav_picture.user == user
    assert fav_picture.foreign_id == FOREIGN_ID
    assert fav_picture.url == URL


def test_fav_picture_model_str(user_data: dict[str, Any]) -> None:
    """Test FavouritePicture model string representation."""
    user = User.objects.create_user(**user_data)

    fav_picture = FavouritePicture.objects.create(
        user=user,
        foreign_id=FOREIGN_ID,
        url=URL,
    )

    fav_picture_str = '<Picture {0} by {1}>'.format(FOREIGN_ID, user.id)

    assert str(fav_picture) == fav_picture_str

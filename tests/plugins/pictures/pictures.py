from typing import TypedDict
import pytest

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


class FavouritePictureData(TypedDict):
    user: User
    foreign_id: int
    url: str


@pytest.fixture
def picture_factory():
    def factory(
            favourite_picture: FavouritePictureData) -> FavouritePicture:
        return FavouritePicture.objects.create(
            **favourite_picture
        )
    return factory


def assert_favourite_picture():
    def assert_model(
        favourite_picture_id: int,
        expected: FavouritePictureData
    ):
        favourite_picture = FavouritePicture.objects.filter(
            id=favourite_picture_id)
        assert favourite_picture.id
        if expected:
            for field_name, data_value in expected.items():
                assert getattr(favourite_picture, field_name) == data_value
    return assert_model

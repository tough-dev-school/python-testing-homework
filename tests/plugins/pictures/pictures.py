from typing import TypedDict
import pytest

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


class FavouritePictureData(TypedDict):
    user: User
    foreign_id: int
    url: str


@pytest.fixture
def favourite_picture_data(create_user):
    # ! рекомендую перейти по ссылке :)
    return FavouritePictureData(
        user=create_user,
        foreign_id=1,
        url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    )


@pytest.fixture
def picture_factory():
    def factory(
            favourite_picture: FavouritePictureData) -> FavouritePicture:
        return FavouritePicture.objects.create(
            **favourite_picture
        )
    return factory


@pytest.fixture
def assert_favourite_picture():
    def factory(
        favourite_picture: FavouritePicture,
        expected: FavouritePictureData
    ):
        # favourite_picture = FavouritePicture.objects.filter(
        #     id=favourite_picture_id)
        assert favourite_picture.id
        for field_name, data_value in expected.items():
            assert getattr(favourite_picture, field_name) == data_value
    return factory

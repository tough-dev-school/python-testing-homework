import pytest

from server.apps.identity.models import User
from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
)
from server.apps.pictures.models import FavouritePicture
from server.common.pydantic_model import BaseModel


class FavouritePictureData(BaseModel):
    """Favourite picture data structure without user."""

    foreign_id: int
    url: str


@pytest.fixture()
def favourite_picture_data() -> FavouritePictureData:
    """Favourite picture example."""
    return FavouritePictureData(
        foreign_id=1,
        url='http://abc.dex',
    )


@pytest.fixture()
def picture_response() -> PictureResponse:
    """Picture service response."""
    return PictureResponse(id=1, url='http://aaa')


@pytest.fixture()
def one_user_favourite(user: User) -> None:
    """Add one favourite picture to user."""
    pic = FavouritePicture(user=user, foreign_id=1, url='http://bbb')
    pic.save()
    yield pic
    pic.delete()

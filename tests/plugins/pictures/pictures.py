from typing import Iterator
import pytest
from mimesis.schema import Field

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
def favourite_picture_data(mfield: Field) -> FavouritePictureData:
    """Favourite picture example."""
    return FavouritePictureData(
        foreign_id=mfield('numeric.increment'),
        url=mfield('internet.uri'),
    )


@pytest.fixture()
def picture_response(mfield: Field) -> PictureResponse:
    """Picture service response."""
    return PictureResponse(
        id=mfield('numeric.increment'),
        url=mfield('internet.uri'),
    )


@pytest.fixture()
def one_user_favourite(
    signedin_user: User,
    mfield: Field,
) -> Iterator[FavouritePicture]:
    """Add one favourite picture to user."""
    picture = FavouritePicture(
        user=signedin_user,
        foreign_id=mfield('numeric.increment'),
        url=mfield('internet.uri'),
    )
    picture.save()
    yield picture
    picture.delete()

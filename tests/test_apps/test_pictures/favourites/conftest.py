from typing import Any, Callable, Generator

import pytest
from typing_extensions import TypeAlias

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from tests.plugins.pictures.picture import PictureData

PictureInContentAssertion: TypeAlias = Callable[[Any, FavouritePicture], None]


@pytest.fixture()
def db_picture(
    db_user: User,
    picture_data: PictureData,
) -> Generator[FavouritePicture, None, None]:
    """Created favourite picture model in database."""
    picture = FavouritePicture.objects.create(user=db_user, **picture_data)
    yield picture
    picture.delete()


@pytest.fixture(scope='session')
def assert_picture_in_content() -> PictureInContentAssertion:
    """Assert that picture is located in response content."""

    def factory(resp_content: Any, picture: FavouritePicture) -> None:
        content_decoded = resp_content.decode()
        assert str(picture.foreign_id) in content_decoded
        assert picture.url in content_decoded

    return factory

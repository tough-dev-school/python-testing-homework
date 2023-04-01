from typing import Callable, List

import pytest
import requests
from typing_extensions import TypeAlias

from config.settings import SETTINGS
from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from tests.plugins.pictures.picture import (
    ExternalAPIPictureData,
    PictureData,
    PictureDataFactory,
)

PicturesAssertion: TypeAlias = Callable[[User], None]


@pytest.fixture(params=['foreign_id', 'url'])
def picture_data_without_req_field(
    picture_data_factory: PictureDataFactory,
    request: pytest.FixtureRequest,
) -> PictureData:
    """Parametrized picture data with 1 missing required field."""
    field = request.param
    return picture_data_factory(**{field: ''})


@pytest.fixture(scope='session')
def assert_no_pictures_loaded() -> PicturesAssertion:
    """Assert that no pictures are loaded for the user."""

    def factory(user: User) -> None:
        pictures_db = FavouritePicture.objects.filter(user=user)
        assert not pictures_db

    return factory


@pytest.fixture(scope='session')
def assert_picture_loaded() -> PicturesAssertion:
    """Assert that picture is loaded for the user."""

    def factory(user: User) -> None:
        FavouritePicture.objects.get(user=user)

    return factory


@pytest.fixture()
def photos_external_api() -> List[ExternalAPIPictureData]:
    """Get photos from external JSON Server API."""
    return requests.get(
        url=SETTINGS.JSON_SERVER_PHOTOS_URL,
        timeout=SETTINGS.JSON_SERVER_TIMEOUT,
    ).json()

import json
from typing import Protocol, TypedDict, final, Callable, Generator

import httpretty
import pytest
from django.conf import settings
from django.test import Client
from mimesis import Field, Schema
from mimesis.enums import Locale
from typing_extensions import Unpack

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from tests.plugins.constants import URL_HTTPRETTY_FINAL


@final
class PictureData(TypedDict, total=False):
    """
    Represent the picture data that is required add favorite pictures.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    foreign_id: int
    url: str


@final
class PictureDataFactory(Protocol):
    """Makes picture data."""

    def __call__(
        self,
        **fields: Unpack[PictureData],
    ) -> PictureData:
        """Picture data factory protocol."""


@pytest.fixture()
def picture_data_factory(
    faker_seed: int,
) -> PictureDataFactory:
    """Returns factory for fake random data for picture."""

    def factory(**fields: Unpack[PictureData]) -> PictureData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'foreign_id': mf('integer_number'),
                'url': mf('url'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory


@pytest.fixture()
def picture_data(picture_data_factory) -> PictureData:
    """Creates picture data for post queries."""
    return picture_data_factory()


@pytest.mark.django_db()
@pytest.fixture()
def picture_creation(
    client: Client,
    picture_data: 'PictureData',
    user_registration: User,
) -> Generator[FavouritePicture, None, None]:
    """Picture creation fixture."""
    favourite_picture_data = {
        **picture_data,
        **{'user': user_registration},
    }
    favourite_picture: FavouritePicture = FavouritePicture.objects. \
        create(**favourite_picture_data)

    yield favourite_picture

    FavouritePicture.objects. \
        filter(foreign_id=favourite_picture.foreign_id).delete()


@pytest.fixture()
def mock_pictures_service() -> Callable[[any], None]:
    """Mock external pictures service using httpretty."""

    def factory(body_object: any) -> None:
        settings.PLACEHOLDER_API_URL = URL_HTTPRETTY_FINAL
        httpretty.register_uri(
            httpretty.GET,
            '{0}photos'.format(URL_HTTPRETTY_FINAL),
            body=json.dumps(body_object),
        )

    return factory

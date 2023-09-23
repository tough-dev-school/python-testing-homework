import json
from typing import Generator, final, Protocol, TypedDict, Any
from urllib.parse import urljoin

import httpretty
import pytest
from mimesis import Field, Locale, Schema

from server.apps.pictures.intrastructure.services.placeholder import PictureResponse
from server.common.django.types import Settings


@final
class PicturesData(TypedDict, total=False):
    """Represent the pictures data response."""

    id: int
    url: str


@final
class PicturesDataFactory(Protocol):
    """Pictures data factory protocol."""

    def __call__(self, iterations: int) -> list[PicturesData]:
        """Pictures data factory protocol."""


@pytest.fixture()
def pictures_data_factory(seed: int) -> PicturesDataFactory:
    def factory(iterations: int) -> list[PicturesData]:
        field = Field(locale=Locale.EN, seed=seed)
        schema = Schema(
            schema=lambda:
            {
                'id': field('numeric.increment'),
                'url': str(field('url')),
            },
            iterations=iterations,
        )
        return schema.create()

    return factory


@pytest.fixture()
def seed() -> int:
    """Seed for generation random data."""
    return Field()('integer_number')


@pytest.fixture()
def expected_pictures_response(
    pictures_data_factory: PicturesDataFactory,
) -> list[PictureResponse]:
    """Create fake external pictures api response, 10 elements."""
    pictures = pictures_data_factory(iterations=10)
    return [PictureResponse(**pic) for pic in pictures]


@pytest.fixture()
def expected_picture_response(
    pictures_data_factory: PicturesDataFactory,
) -> PictureResponse:
    """Create fake external pictures api response, 1 element."""
    picture = pictures_data_factory(iterations=1)
    return PictureResponse(**picture[0])


@pytest.fixture()
def failed_pydantic_fields(
) -> dict[str, Any]:
    """Return failed fields for pydantic validations."""
    return {'TEST': 1}


@pytest.fixture()
def mock_pictures_api(
    settings: Settings,
    expected_pictures_response: list[PictureResponse],
) -> Generator:
    """Mock external `PLACEHOLDER_API_URL` calls."""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.GET,
            body=json.dumps([picture.model_dump() for picture in expected_pictures_response]),
            uri=urljoin(settings.PLACEHOLDER_API_URL, "/photos"),
        )
        yield expected_pictures_response
        assert httpretty.has_request()

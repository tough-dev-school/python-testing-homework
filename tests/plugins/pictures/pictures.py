import json
from typing import TypedDict, cast, Generator

import httpretty
import pytest
from mimesis import Field, Locale, Schema

from server.common.django.types import Settings


class PicturesAPIResponse(TypedDict):
    """Response from pictures service api."""
    id: int
    url: str


@pytest.fixture()
def seed() -> int:
    """Seed for generation random data."""
    return Field()('integer_number')


@pytest.fixture()
def expected_pictures_response(seed: int) -> list[PicturesAPIResponse]:
    """Create fake external pictures api response."""
    field = Field(locale=Locale.EN, seed=seed)
    schema = Schema(
        schema=lambda:
        {
            'id': field('numeric.increment'),
            'url': str(field('url')),
        },
    )
    return cast(list[PicturesAPIResponse], list(schema.create()))


@pytest.fixture()
def mock_pictures_api(
    settings: Settings,
    expected_pictures_response: list[PicturesAPIResponse],
) -> Generator:
    """Mock external `PLACEHOLDER_API_URL` calls."""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.GET,
            body=json.dumps(expected_pictures_response),
            uri=settings.PLACEHOLDER_API_URL,
        )
        yield expected_pictures_response
        assert httpretty.has_request()

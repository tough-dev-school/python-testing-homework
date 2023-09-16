import json
import re
from re import Pattern
from typing import Iterator, Any

import httpretty
import pytest
from mimesis import Field, Schema, Locale
from typing_extensions import TypedDict

from server.apps.pictures.container import container
from server.apps.pictures.logic.usecases import pictures_fetch
from server.common.django.types import Settings


class PicturesAPIResponse(TypedDict):
    id: int
    url: str


@pytest.fixture
def seed() -> int:
    return Field()('integer_number')


@pytest.fixture
def pictures_expected_api_response(seed: int) -> list[PicturesAPIResponse]:
    """Create fake external api response for pictures."""

    mf = Field(locale=Locale.EN, seed=seed)
    schema = Schema(
        schema=lambda:
        {
            'id': str(mf('numeric.increment')),
            'url': str(mf('url')),
        },
    )
    return list(schema.create())


@pytest.fixture
def pictures_api_mock(
    settings: Settings,
    pictures_expected_api_response: list[PicturesAPIResponse],
) -> Iterator[list[PicturesAPIResponse]]:
    """Mock external `PLACEHOLDER_API_URL/*` calls."""
    with httpretty.httprettized():
        _mock_pictures_api(pictures_expected_api_response, re.compile(rf'{settings.PLACEHOLDER_API_URL}.*'))
        yield
        assert httpretty.has_request()


@pytest.fixture
def pictures_api_mock_corrupted(
    settings: Settings,
) -> Iterator[list[PicturesAPIResponse]]:
    """Mock external `PLACEHOLDER_API_URL/*` calls, call returns invalid data"""
    with httpretty.httprettized():
        invalid_data = [{}]
        _mock_pictures_api(invalid_data, re.compile(rf'{settings.PLACEHOLDER_API_URL}.*'))
        yield


def _mock_pictures_api(mocked_response: list[Any], api_url: Pattern[str]):
    httpretty.register_uri(
        method=httpretty.GET,
        body=json.dumps(mocked_response),
        uri=api_url,
    )


@pytest.fixture
def pictures_service() -> pictures_fetch.PicturesFetch:
    """Get pictures service."""
    return container.instantiate(pictures_fetch.PicturesFetch)

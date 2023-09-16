import json
import re
from typing import Any, Iterator, cast

import httpretty
import pytest
from mimesis import Field, Locale, Schema
from typing_extensions import TypedDict

from server.apps.pictures.container import container
from server.apps.pictures.logic.usecases import pictures_fetch
from server.common.django.types import Settings


class PicturesAPIResponse(TypedDict):
    """Representation of single object from pictures service api."""

    id: int
    url: str


@pytest.fixture()
def seed() -> int:
    """Seed for generation random data."""
    return Field()('integer_number')


@pytest.fixture()
def pictures_expected_api_response(seed: int) -> list[PicturesAPIResponse]:
    """Create fake external api response for pictures."""
    mf = Field(locale=Locale.EN, seed=seed)
    schema = Schema(
        schema=lambda:
        {
            'id': mf('numeric.increment'),
            'url': str(mf('url')),
        },
    )
    return cast(list[PicturesAPIResponse], list(schema.create()))


@pytest.fixture()
def api_url(settings: Settings) -> re.Pattern[str]:
    """Regex of picture API url."""
    return re.compile(f'{settings.PLACEHOLDER_API_URL}.*')


@pytest.fixture()
def _pictures_api_mock(
    api_url: re.Pattern[str],
    pictures_expected_api_response: list[PicturesAPIResponse],
) -> Iterator[None]:
    """Mock external `PLACEHOLDER_API_URL/*` calls."""
    with httpretty.httprettized():
        _mock_pictures_api(pictures_expected_api_response, api_url)
        yield
        assert httpretty.has_request()


@pytest.fixture()
def _pictures_api_mock_corrupted(
    api_url: re.Pattern[str],
) -> Iterator[None]:
    """Mock external `PLACEHOLDER_API_URL/*` calls, returns invalid data."""
    with httpretty.httprettized():
        invalid_data: list[dict[str, Any]] = [{}]
        _mock_pictures_api(invalid_data, api_url)
        yield


def _mock_pictures_api(mocked_response: list[Any], api_url: re.Pattern[str]) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        body=json.dumps(mocked_response),
        uri=api_url,
    )


@pytest.fixture()
def pictures_service() -> pictures_fetch.PicturesFetch:
    """Get pictures service."""
    return container.instantiate(pictures_fetch.PicturesFetch)

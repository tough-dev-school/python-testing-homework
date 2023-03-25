import re
from contextlib import contextmanager
from typing import Callable, Iterator, List
from urllib.parse import urljoin

import httpretty
import pytest

from server.apps.pictures.container import container
from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
)
from server.apps.pictures.logic.usecases.pictures_fetch import PicturesFetch
from server.common.django.types import Settings
from server.common.pydantic_model import BaseModel


class PictureResponsesList(BaseModel):
    """Structure for response."""

    __root__: List[PictureResponse]


@pytest.fixture()
def mock_pictures_fetch_api(
    settings: Settings,
) -> Callable[[List[PictureResponse]], None]:
    """Mock placeholder API endpoint."""

    @contextmanager
    def factory(response: List[PictureResponse]) -> Iterator[None]:
        mock_response = PictureResponsesList(__root__=response)
        mock_url = urljoin(settings.PLACEHOLDER_API_URL, '.*')
        with httpretty.httprettized():
            httpretty.register_uri(
                httpretty.GET,
                re.compile(mock_url),
                body=mock_response.json(),
                content_type='application/json',
            )
            yield
            assert httpretty.has_request()
    return factory


def test_lead_mock_structure(
    picture_response: PictureResponse,
    mock_pictures_fetch_api,
) -> None:
    """Ensure the returned structure from the mocked image fetcher."""
    dummy_pictures: List[PictureResponse] = [picture_response]
    pictures_fetcher: PicturesFetch = container.instantiate(PicturesFetch)

    with mock_pictures_fetch_api(response=dummy_pictures):
        got_pictures = pictures_fetcher(5)

    assert len(got_pictures) == 1
    assert got_pictures[0].id == dummy_pictures[0].id
    assert got_pictures[0].url == dummy_pictures[0].url

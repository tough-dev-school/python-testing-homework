import re
from typing import List
from urllib.parse import urljoin

import httpretty

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


def mock_pictures_fetch_dummy_response(
    response: List[PictureResponse],
    settings: Settings,
) -> None:
    """Mock placeholder API endpoint."""
    mock_response = PictureResponsesList(__root__=response)
    mock_url = urljoin(settings.PLACEHOLDER_API_URL, '.*')
    httpretty.register_uri(
        httpretty.GET,
        re.compile(mock_url),
        body=mock_response.json(),
        content_type='application/json',
    )


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_pictures_correct_mock_structure(
    picture_response: PictureResponse,
    settings: Settings,
) -> None:
    """Ensure the returned structure from the mocked image fetcher."""
    dummy_pictures: List[PictureResponse] = [picture_response]
    mock_pictures_fetch_dummy_response(
        response=dummy_pictures,
        settings=settings,
    )
    pictures_fetcher: PicturesFetch = container.instantiate(PicturesFetch)

    got_pictures = pictures_fetcher(5)

    assert len(got_pictures) == 1
    assert got_pictures[0].id == dummy_pictures[0].id
    assert got_pictures[0].url == dummy_pictures[0].url

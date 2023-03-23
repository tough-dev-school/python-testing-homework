import re
from typing import List
from urllib.parse import urljoin
import httpretty

from server.apps.pictures.container import container
from server.apps.pictures.intrastructure.services.placeholder import PictureResponse
from server.apps.pictures.logic.usecases.pictures_fetch import PicturesFetch
from server.apps.pictures.intrastructure.services.placeholder import PicturesFetch as PicturesFetchPlaceholder

from server.common.django.types import Settings
from server.common.pydantic_model import BaseModel


class PictureResponsesList(BaseModel):
    __root__: List[PictureResponse]


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_mock_structure1() -> None:
    """Ensure the returned structure from the mocked image fetcher."""
    settings: Settings = container.resolve(Settings)
    dummy_pictures: List[PictureResponse] = [PictureResponse(id=1, url='http://aaa')]
    resp = PictureResponsesList(__root__=dummy_pictures)
    mock_url = urljoin(settings.PLACEHOLDER_API_URL, PicturesFetchPlaceholder._url_path)
    httpretty.register_uri(
        httpretty.GET,
        mock_url,
        body=resp.json(),
        content_type='application/json',
    )
    pictures_fetcher = container.instantiate(PicturesFetch)

    got_pictures = pictures_fetcher(5)

    assert len(got_pictures) == 1
    assert got_pictures[0].id == dummy_pictures[0].id



@httpretty.activate(verbose=True, allow_net_connect=False)
def test_mock_structure2() -> None:
    """Ensure the returned structure from the mocked image fetcher."""
    settings: Settings = container.resolve(Settings)
    dummy_pictures: List[PictureResponse] = [PictureResponse(id=1, url='http://aaa')]
    resp = PictureResponsesList(__root__=dummy_pictures)
    mock_url = urljoin(settings.PLACEHOLDER_API_URL, '.*')
    httpretty.register_uri(
        httpretty.GET,
        re.compile(mock_url),
        body=resp.json(),
        content_type='application/json',
    )
    pictures_fetcher = container.instantiate(PicturesFetch)

    got_pictures = pictures_fetcher(5)

    assert len(got_pictures) == 1
    assert got_pictures[0].id == dummy_pictures[0].id


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_mock_structure3() -> None:
    """Ensure the returned structure from the mocked image fetcher."""
    settings: Settings = container.resolve(Settings)
    dummy_pictures: List[PictureResponse] = [PictureResponse(id=1, url='http://aaa')]
    resp = PictureResponsesList(__root__=dummy_pictures)
    mock_url = urljoin(settings.PLACEHOLDER_API_URL, PicturesFetchPlaceholder._url_path)
    httpretty.register_uri(
        httpretty.GET,
        mock_url,
        body=resp.json(),
        content_type='application/json',
    )
    pictures_fetcher = PicturesFetchPlaceholder(api_url=settings.PLACEHOLDER_API_URL, api_timeout=settings.PLACEHOLDER_API_TIMEOUT)

    got_pictures = pictures_fetcher(limit=5)

    assert len(got_pictures) == 1
    assert got_pictures[0].id == dummy_pictures[0].id

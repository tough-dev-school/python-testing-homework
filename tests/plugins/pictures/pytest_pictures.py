import re
from typing import List
from urllib.parse import urljoin

import httpretty
import pytest

from server.apps.identity.models import User
from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
)
from server.apps.pictures.models import FavouritePicture
from server.common.django.types import Settings
from server.common.pydantic_model import BaseModel


class FavouritePictureData(BaseModel):
   foreign_id: int
   url: str


@pytest.fixture()
def favourite_picture_data() -> FavouritePictureData:
   return FavouritePictureData(
      foreign_id=1,
      url='http://abc.dex',
   )


@pytest.fixture()
def picture_response() -> PictureResponse:
   return PictureResponse(id=1, url='http://aaa')



@pytest.fixture()
def one_user_favourite(user: User) -> None:
    pic = FavouritePicture(user=user, foreign_id=1, url='http://bbb')
    pic.save()
    yield pic
    pic.delete()


class PictureResponsesList(BaseModel):
    __root__: List[PictureResponse]


def mock_pictures_fetch_dummy_response(
    response: List[PictureResponse],
    settings: Settings,
) -> None:
    mock_response = PictureResponsesList(__root__=response)
    mock_url = urljoin(settings.PLACEHOLDER_API_URL, '.*')
    httpretty.register_uri(
        httpretty.GET,
        re.compile(mock_url),
        body=mock_response.json(),
        content_type='application/json',
    )

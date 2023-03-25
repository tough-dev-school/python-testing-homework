import json

import httpretty
from django.conf import settings

from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
    PicturesFetch,
)


@httpretty.activate
def test_image_request(picture_data_factory):
    httpretty.register_uri(
        httpretty.GET,
        f"{settings.PLACEHOLDER_API_URL}/photos",
        body=json.dumps(picture_data_factory(count_factory=2)),
    )
    response = PicturesFetch()()
    result = response.json() 

    assert len(result) == 2
    assert isinstance(result[0], PictureResponse)

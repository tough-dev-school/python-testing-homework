import pytest

from mimesis import Internet, Numeric

from server.apps.pictures.intrastructure.services.placeholder import PictureResponse


@pytest.fixture()
def favourites_endpoint() -> str:
    return '/pictures/favourites'


@pytest.fixture()
def picture_response() -> PictureResponse:
    return PictureResponse(id=Numeric().increment(), url=Internet().uri())



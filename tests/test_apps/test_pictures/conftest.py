import pytest

from tests.plugins.pictures.picture import PictureData, PictureDataFactory


@pytest.fixture()
def picture_data(picture_data_factory: PictureDataFactory) -> PictureData:
    """Picture data with all required fields."""
    return picture_data_factory()

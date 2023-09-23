from typing import Any

import pytest
from pydantic import ValidationError

from server.apps.pictures.intrastructure.services.placeholder import PicturesFetch, PictureResponse
from server.common.django.types import Settings
from tests.plugins.pictures.pictures import PicturesDataFactory


def test_pictures_fetch_service(
    settings: Settings,
    seed: int,
    expected_pictures_response: list[PictureResponse],
    mock_pictures_api,
) -> None:
    """Test Pictures Fetch service."""
    actual_picture_response = PicturesFetch(
        api_url=settings.PLACEHOLDER_API_URL,
        api_timeout=settings.PLACEHOLDER_API_TIMEOUT,
    )(limit=seed)
    assert actual_picture_response == expected_pictures_response


def test_success_validate_pictures_response(
    expected_picture_response: PictureResponse,
    pictures_data_factory: PicturesDataFactory,
) -> None:
    """Testing PictureResponse model, success case."""
    actual_picture_response = PictureResponse.model_validate(
        pictures_data_factory(iterations=1)[0]
    )
    assert actual_picture_response == expected_picture_response


def test_failed_validate_pictures_response(
    failed_pydantic_fields: dict[str, Any],
) -> None:
    """Testing PictureResponse model, failed case."""
    with pytest.raises(ValidationError):
        PictureResponse.model_validate(failed_pydantic_fields)  # noqa: WPS428

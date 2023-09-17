import httpretty
import pytest
from pydantic import TypeAdapter

from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
)
from server.apps.pictures.logic.usecases import pictures_fetch

from .conftest import PicturesAPIResponse


class TestPicturesFetchServiceMockedAPI:
    """Test with mocked API."""

    @pytest.mark.usefixtures('_pictures_api_mock')
    def test_service_fetches_expected_pictures(
        self,
        pictures_expected_api_response: list[PicturesAPIResponse],
        pictures_service: pictures_fetch.PicturesFetch,
    ) -> None:
        """Check that API call returns pictures in expected form."""
        pictures_from_service: list[PictureResponse] = pictures_service()
        type_adapter = TypeAdapter(list[PictureResponse])
        deserialized_pictures_from_net: list[PictureResponse] = (
            type_adapter.validate_python(pictures_expected_api_response)
        )

        assert pictures_from_service == deserialized_pictures_from_net
        assert '_limit' in httpretty.last_request().querystring

    @pytest.mark.usefixtures('_pictures_api_mock_corrupted')
    def test_service_raises_value_error_on_invalid_data(
        self,
        pictures_service: pictures_fetch.PicturesFetch,
    ) -> None:
        """Check that service raises ValueError when fetched data is invalid."""
        with pytest.raises(ValueError):
            pictures_service()


@pytest.mark.webtest()
class TestPicturesFetchServiceRealAPI:
    """Test with real API."""

    @pytest.mark.parametrize('limit', [1, 3, 5, 10, 15])
    def test_limit_query_params_limits_response_size(
        self,
        limit: int,
        pictures_service: pictures_fetch.PicturesFetch,
    ) -> None:
        """Tests `limit` query param."""
        pictures = pictures_service(limit)
        assert len(pictures) == limit

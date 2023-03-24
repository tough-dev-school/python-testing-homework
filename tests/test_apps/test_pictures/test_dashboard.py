import json
from http import HTTPStatus
from typing import TYPE_CHECKING, Callable

import httpretty
import pytest
import requests
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.intrastructure.services.placeholder import (
    PictureResponse,
)
from server.apps.pictures.models import FavouritePicture
from server.apps.pictures.views import DashboardView

if TYPE_CHECKING:
    from plugins.pictures.picture import PictureData


@pytest.fixture()
def external_api_photos_response(
    external_api_url_factory: Callable[[str], str],
) -> 'PictureData':
    """Get photos from json-server."""
    connection_limit_in_sec = 2
    execution_limit_in_sec = 5
    return requests.get(
        url=external_api_url_factory('photos'),
        timeout=(connection_limit_in_sec, execution_limit_in_sec),
    ).json()


@pytest.mark.usefixtures('_unauthorized_client')
@pytest.mark.django_db()
class TestPicturesDashboard(object):
    """A class for testing the logic of dashboard pictures."""

    _url = reverse('pictures:dashboard')

    def test_view_dashboard_renders(
        self,
        get_user: User,
        picture_data: 'PictureData',
    ) -> None:
        """Test correct picture adding."""
        # Arrange
        self.client.force_login(get_user)

        # Act
        response = self.client.post(self._url, data=picture_data)
        resolver_func = response.resolver_match.func.__name__

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('pictures:dashboard')
        assert resolver_func == DashboardView.as_view().__name__
        assert FavouritePicture.objects.get(user=get_user)

    @pytest.mark.slow()
    @pytest.mark.flaky(retries=3, delay=1)
    @httpretty.activate
    def test_pictures_external_api(
        self,
        get_user: User,
        external_api_url_factory: Callable[[str], str],
        external_api_photos_response,
    ) -> None:
        """Check dashboard content."""
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=external_api_url_factory('photos'),
            body=json.dumps(external_api_photos_response),
            content_type='application/json',
        )
        self.client.force_login(get_user)

        # Act
        response = self.client.get(self._url)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert httpretty.last_request().method == 'GET'
        assert '/photos' in httpretty.last_request().path
        assert response.context['pictures'] == external_api_photos_response
        assert len(response.context['pictures']) == (
            len(external_api_photos_response)
        )
        for picture in response.context['pictures']:
            assert isinstance(picture, PictureResponse)

import json
from http import HTTPStatus
from typing import List

import httpretty
import pytest
from django.test import Client
from django.urls import reverse

from config.settings import SETTINGS
from server.apps.identity.models import User
from tests.plugins.pictures.picture import ExternalAPIPictureData, PictureData
from tests.test_apps.test_pictures.dashboard.conftest import PicturesAssertion

URL_PATH = reverse('pictures:dashboard')


@pytest.mark.django_db()
def test_not_logined_redirect(client: Client) -> None:
    """Endpoint redirects if user is not logined."""
    response = client.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_page_renders(client_logined: Client) -> None:
    """Basic `get` method works if user is logined."""
    response = client_logined.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_add_picture_no_required_field(
    client_logined: Client,
    db_user: User,
    picture_data_without_req_field: PictureData,
    assert_no_pictures_loaded: PicturesAssertion,
) -> None:
    """Picture addition fails is any required field is not provided."""
    response = client_logined.post(
        path=URL_PATH,
        data=picture_data_without_req_field,
    )
    assert response.status_code == HTTPStatus.OK
    assert_no_pictures_loaded(db_user)


@pytest.mark.django_db()
def test_add_picture_valid(
    client_logined: Client,
    db_user: User,
    picture_data: PictureData,
    assert_picture_loaded: PicturesAssertion,
) -> None:
    """Picture addition is successful if all required fields are provided."""
    response = client_logined.post(
        path=URL_PATH,
        data=picture_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert_picture_loaded(db_user)


@pytest.mark.django_db()
@pytest.mark.slow()
@httpretty.activate
def test_dashboard_external_api(
    client_logined: Client,
    photos_external_api: List[ExternalAPIPictureData],
) -> None:
    """
    Dashboard pictures display is successful if using external API.

    Photos API url is redirected to external JSON Server.
    """
    httpretty.register_uri(
        method=httpretty.GET,
        uri=SETTINGS.DJANGO_PHOTOS_API_URL,
        body=json.dumps(photos_external_api),
        content_type='application/json',
    )
    response = client_logined.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.OK
    assert response.context['pictures'] == photos_external_api

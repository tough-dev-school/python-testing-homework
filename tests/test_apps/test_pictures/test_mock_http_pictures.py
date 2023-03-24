import json
import os
from http import HTTPStatus
from typing import TYPE_CHECKING, Final
from urllib.parse import urljoin

if TYPE_CHECKING:
    from plugins.identity.user import RegistrationData
    from plugins.identity.user import UserData

import httpretty
import pytest
import requests
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

PROTOKOL: Final = 'http'


@pytest.fixture()
def json_server():
    """Get photos from json-server."""
    return requests.get(
        f'{PROTOKOL}://{os.getenv("JSON_SERVER_NAME")}/photos',
        timeout=3,
    ).json()


@pytest.mark.django_db()
@httpretty.activate
def test_pictures_dashboard_content(
    get_user: User,
    client: Client,
    json_server,
) -> None:
    """Check dashboard content."""
    # Arrange
    httpretty.register_uri(
        method=httpretty.GET,
        uri=urljoin(os.environ["DJANGO_PLACEHOLDER_API_URL"], 'photos'),
        body=json.dumps(json_server),
        content_type='application/json',
    )
    client.force_login(get_user)

    # Act
    response = client.get(reverse('pictures:dashboard'))

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.context['pictures'] == json_server
    assert len(response.context['pictures']) == len(json_server)


@pytest.fixture()
def json_server_users(registration_data: 'RegistrationData'):
    """Get photos from json-server."""
    registration_data['date_of_birth'] = str(registration_data['date_of_birth'])
    return requests.post(
        f'{PROTOKOL}://{os.getenv("JSON_SERVER_NAME")}/users',
        json=registration_data,
        timeout=4,
    ).json()


@pytest.mark.django_db()
@httpretty.activate
def test_users_adding(
    client: Client,
    user_data: 'UserData',
    registration_data: 'RegistrationData',
    json_server_users,
) -> None:
    """Check users adding from json-server."""
    # Arrange
    httpretty.register_uri(
        method=httpretty.POST,
        uri=urljoin(os.environ["DJANGO_PLACEHOLDER_API_URL"], 'users'),
        body=json.dumps(json_server_users, default=str),
        content_type='application/json',
    )

    # Act
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    # Assert
    assert response.status_code == HTTPStatus.FOUND

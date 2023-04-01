import json
import os
from http import HTTPStatus
from typing import TYPE_CHECKING
from urllib.parse import urljoin

if TYPE_CHECKING:
    from tests.plugins.identity.user import UserData, RegistrationData

import httpretty
import pytest
import requests
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.fixture()
def json_server_photos():
    """Get photos from json_server."""
    return requests.get(
        f'http://{os.environ["JSON_SERVER_NAME"]}/photos',
        timeout=3,
    ).json()


@pytest.mark.django_db()
@httpretty.activate
def test_pictures_dashboard_content(
    db_user: 'UserData',
    client: Client,
    json_server_photos,
) -> None:
    """Check dashboard content."""
    httpretty.register_uri(
        httpretty.GET,
        urljoin(os.environ["DJANGO_PLACEHOLDER_API_URL"], 'photos'),
        body=json.dumps(json_server_photos),
        content_type='application/json',
    )
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)

    response = client.get(reverse('pictures:dashboard'))
    assert response.status_code == HTTPStatus.OK
    assert len(response.context['pictures']) == len(json_server_photos)
    assert response.context['pictures'] == json_server_photos


@pytest.fixture()
def json_server_users(registration_data):
    """Get photos from json_server."""
    registration_data['date_of_birth'] = str(registration_data['date_of_birth'])
    return requests.post(
        f'http://{os.environ["JSON_SERVER_NAME"]}/users',
        json=registration_data,
        timeout=4,
    ).json()


@pytest.mark.django_db()
@httpretty.activate
def test_users_adding(
    client: Client,
    user_data: 'User',
    registration_data: 'RegistrationData',
    json_server_users,
) -> None:
    """Check users adding."""
    httpretty.register_uri(
        httpretty.POST,
        urljoin(os.environ["DJANGO_PLACEHOLDER_API_URL"], 'users'),
        body=json.dumps(json_server_users, default=str),
        content_type='application/json',
    )

    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND

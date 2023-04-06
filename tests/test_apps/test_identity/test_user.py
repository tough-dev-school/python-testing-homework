from http import HTTPStatus
from typing import Callable, Iterator

import httpretty
import pytest
import requests
from django.conf import settings
from django.test import Client

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.apps.identity.models import User
from tests.plugins.identity.users import RegistrationData
from tests.utils import mock_external_endpoint

UserAssertion = Callable[[str, int], None]
LeadAssertion = Callable[[str], None]


@pytest.fixture(scope='session')
def assert_regular_user_exists() -> UserAssertion:
    def factory(email: str, lead_id: int) -> None:
        user = User.objects.get(email=email)
        assert user.lead_id == lead_id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

    return factory


@pytest.fixture()
def assert_lead_on_server(json_server: str) -> LeadAssertion:
    def factory(email: str) -> None:
        leads = requests.get(f'{json_server}/users').json()
        assert email in {lead['email'] for lead in leads}

    return factory


@pytest.fixture()
def json_server() -> Iterator[str]:
    json_server_url = 'http://localhost:3000'
    previous = settings.PLACEHOLDER_API_URL
    settings.PLACEHOLDER_API_URL = json_server_url
    yield json_server_url
    settings.PLACEHOLDER_API_URL = previous


@pytest.fixture()
def create_lead_mock(user_id_response: UserResponse) -> Iterator[UserResponse]:
    """Mock external `/user/register` calls."""
    endpoint = '/users'
    method = httpretty.POST
    response_body = user_id_response

    with mock_external_endpoint(method, endpoint, response_body):
        yield user_id_response


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: RegistrationData,
    assert_regular_user_exists: UserAssertion,
    create_lead_mock: UserResponse,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        '/identity/registration',
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert_regular_user_exists(registration_data['email'], create_lead_mock.id)


@pytest.mark.django_db()
def test_lead_saved(
    client: Client,
    registration_data: RegistrationData,
    json_server: str,
    assert_lead_on_server: LeadAssertion,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        '/identity/registration',
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert_lead_on_server(registration_data['email'])

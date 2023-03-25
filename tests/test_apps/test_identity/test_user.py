from http import HTTPStatus
from typing import Callable, Iterator

import httpretty
import pytest
from django.test import Client
from pydantic import BaseModel

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.apps.identity.models import User
from tests.plugins.identity.users import RegistrationData, UserData
from tests.utils import mock_external_endpoint

UserAssertion = Callable[[str, int], None]


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
def create_lead_mock(user_id_response: UserResponse) -> Iterator[UserResponse]:
    """Mock external `/user/register` calls."""
    endpoint = '/users'
    method = httpretty.POST
    response_body = user_id_response

    with mock_external_endpoint(method, endpoint, response_body):
        yield user_id_response


@pytest.fixture()
def _update_lead_mock() -> Iterator[None]:
    """Mock external `/user/register` calls."""
    endpoint = '/users'
    method = httpretty.PATCH

    with mock_external_endpoint(method, endpoint, BaseModel()):
        yield


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
def test_user_update(
    user_client: Client,
    user_data: UserData,
) -> None:
    """Test that registration works with correct user data."""
    response = user_client.post('/identity/update', data=user_data)

    assert response.status_code == HTTPStatus.FOUND

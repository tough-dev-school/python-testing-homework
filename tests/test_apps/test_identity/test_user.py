from contextlib import contextmanager
from http import HTTPStatus
import json
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils.functional import lazy
import httpretty
from pydantic import BaseModel
import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from mimesis import Numeric, Person, Address

from typing import Callable, Iterator
from typing_extensions import Required
from server.apps.identity.intrastructure.services.placeholder import UserResponse

from server.apps.identity.models import User

from datetime import datetime
from typing import Callable, TypedDict, final


class UserData(TypedDict, total=False):
    email: Required[str]
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


@final
class RegistrationData(UserData, total=False):
    password1: str
    password2: str

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
def user_data() -> UserData:
    mf = Field(locale=Locale. RU, seed=123)
    person = Person()
    address = Address()
    return UserData(
        email=person.email(),
        first_name=person.first_name(),
        last_name=person.last_name(),
        date_of_birth=mf('datetime.date'),
        address=address.city(),
        job_title=person.occupation(),
        phone=person.telephone(),
        phone_type=mf('choice', items=[1, 2, 3]),
    )


@pytest.fixture()
def registration_data(user_data: UserData) -> RegistrationData:
    mf = Field(locale=Locale.RU, seed=123)
    password = mf('password')
    return RegistrationData(
        **user_data,
        **{'password1': password, 'password2': password},
    )



@pytest.fixture()
def user_id_response() -> UserResponse:
    return UserResponse(id=Numeric().increment())


@contextmanager
def mock_external_endpoint(method: str, endpoint: str, response_body: BaseModel) -> Iterator[None]:
    with httpretty.httprettized():
        httpretty.register_uri(
            method=method,
            body=response_body.json(),
            uri=settings.PLACEHOLDER_API_URL + endpoint
    )
        yield
        assert httpretty.has_request()


@pytest.fixture()
def create_lead_mock(user_id_response: UserResponse) -> Iterator[UserResponse]:
    """Mock external `/user/register` calls."""
    endpoint = '/users'
    method = httpretty.POST
    response_body = user_id_response

    with mock_external_endpoint(method, endpoint, response_body):
        yield user_id_response

@pytest.fixture()
def update_lead_mock() -> Iterator[None]:
    """Mock external `/user/register` calls."""
    endpoint = '/users'
    method = httpretty.PATCH

    with mock_external_endpoint(method, endpoint, BaseModel()):
        yield None

@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: RegistrationData,
    assert_regular_user_exists: UserAssertion,
    create_lead_mock: UserResponse,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post (
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert_regular_user_exists(registration_data['email'], create_lead_mock.id)


@pytest.mark.django_db()
def test_user_update(
    user_client: Client,
    user_data: UserData,
    update_lead_mock: UserResponse,
) -> None:
    """Test that registration works with correct user data."""
    response = user_client.post('/identity/update', data=user_data)

    assert response.status_code == HTTPStatus.FOUND
    # assert_regular_user_exists(registration_data['email'], create_lead_mock.id)

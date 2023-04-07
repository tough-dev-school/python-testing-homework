import datetime
import re
from contextlib import contextmanager
from http import HTTPStatus
from typing import Callable, Iterator, Protocol, TypedDict, final
from urllib.parse import urljoin

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.common.django.types import Settings

try:
    # Requires Python 3.11
    from typing import Unpack  # noqa: WPS433 # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import Unpack  # noqa: WPS433, WPS440

try:
    # Requires Python 3.10
    from typing import TypeAlias  # noqa: WPS433 # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias  # noqa: WPS433, WPS440

import httpretty
import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field, Schema

from server.apps.identity.models import User


@final
class UserData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class RegistrationData(UserData, total=False):
    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        return RegistrationData(**fields)


@pytest.fixture()
def registration_data_factory(mfield: Field) -> RegistrationDataFactory:
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = mfield('password')
        schema = Schema(schema=lambda: {
            'email': mfield('person.email'),
            'first_name': mfield('person.first_name'),
            'last_name': mfield('person.last_name'),
            'date_of_birth': mfield('datetime.date'),
            'address': mfield('address.address'),
            'job_title': mfield('person.occupation'),
            'phone': mfield('person.telephone'),
        })
        return {
            **schema.create(iterations=1)[0],
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(registration_data_factory: RegistrationDataFactory) -> RegistrationData:
    return registration_data_factory()


ExpectedUserData: TypeAlias = Callable[[RegistrationData], UserData]


@pytest.fixture()
def expected_user_data() -> ExpectedUserData:
    def factory(registration_data: RegistrationData) -> UserData:
        return {  # type: ignore[return-value]
            key_name: value_part
            for key_name, value_part in registration_data.items()
            if not key_name.startswith('password')
        }

    return factory


@final
class SigninUserData(TypedDict, total=False):
    username: str
    password: str


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> User:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value
        return user

    return factory


MockLeadFetchAPI: TypeAlias = Callable[[str, str], None]


@pytest.fixture()
def mock_lead_fetch_api(settings: Settings) -> Iterator[MockLeadFetchAPI]:
    @contextmanager
    def factory(*, method: str, body: str) -> Iterator[None]:
        mock_url = urljoin(settings.PLACEHOLDER_API_URL, '.*')
        with httpretty.httprettized():
            httpretty.register_uri(
                method,
                re.compile(mock_url),
                body=body,
                content_type='application/json',
            )
            yield
            assert httpretty.has_request()

    return factory


MockPostLeadFetchAPI: TypeAlias = Callable[[], None]


@pytest.fixture()
def mock_lead_post_user_api(
    mfield: Field,
    mock_lead_fetch_api: MockLeadFetchAPI
) -> MockPostLeadFetchAPI:
    @contextmanager
    def factory() -> Iterator[None]:
        user_response = UserResponse(id=mfield('numeric.increment'))
        with mock_lead_fetch_api(method=httpretty.POST, body=user_response.json()):
            yield

    return factory


@pytest.fixture()
@pytest.mark.django_db()
def registered_user(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'ExpectedUserData',
    assert_correct_user: 'UserAssertion',
    mock_lead_post_user_api: MockLeadFetchAPI,
) -> User:
    """Test that registration works with correct user data."""
    with mock_lead_post_user_api():
        response = client.post(
            reverse('identity:registration'),
            data=registration_data,
        )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')  # type: ignore[attr-defined]

    return assert_correct_user(registration_data['email'], expected_user_data(registration_data))


@pytest.fixture()
def signin_user_data(registration_data: RegistrationData, registered_user: User) -> SigninUserData:
    return SigninUserData(
        username=registered_user.email,
        password=registration_data['password1'],
    )


@pytest.fixture()
@pytest.mark.django_db()
def sign_user(
    client: Client,
    signin_user_data: SigninUserData,
    registered_user: User,
) -> User:
    response = client.post(
        reverse('identity:login'),
        data=signin_user_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')  # type: ignore[attr-defined]

    return registered_user

import datetime as dt
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
    from typing import Unpack  # noqa: WPS433
except ImportError:
    from typing_extensions import Unpack  # noqa: WPS433, WPS440

try:
    # Requires Python 3.10
    from typing import TypeAlias  # noqa: WPS433
except ImportError:
    from typing_extensions import TypeAlias  # noqa: WPS433, WPS440

import httpretty
import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field, Schema

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """The user data required to create a new user without password."""

    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class RegistrationData(UserData, total=False):
    """Represent the registration data required to create a new user."""

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    """User data factory protocol."""

    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        """Call factory."""
        return RegistrationData(**fields)


@pytest.fixture()
def registration_data_factory(
    mfield: Field,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for regitration."""
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = mfield('password')  # by default passwords are equal
        schema = Schema(schema=lambda: {
            'email': mfield('person.email'),
            'first_name': mfield('person.first_name'),
            'last_name': mfield('person.last_name'),
            'date_of_birth': mfield('datetime.date'),
            'address': mfield('address.address'),
            'job_title': mfield('person.occupation'),
            'phone': mfield('person.telephone'),
        })
        return {  # type: ignore[misc]
            **schema.create(iterations=1)[0],
            **{'password1': password, 'password2': password},
            **fields,
        }
    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Default success registration data."""
    return registration_data_factory()


@final
class SigninUserData(TypedDict, total=False):
    """Represent the signin data."""

    username: str
    password: str


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Assert inserted User and expected data."""
    def factory(email: str, expected: UserData) -> User:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value
        return user
    return factory


MockLeadFetchAPI: TypeAlias = Callable[[str, str], None]


@pytest.fixture()
def mock_lead_fetch_api(
    settings: Settings,
) -> MockLeadFetchAPI:
    """Mock lead API endpoint."""

    @contextmanager
    def factory(*, method: str, body: str) -> None:
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


@pytest.fixture()
def mock_lead_post_user_api(
    mfield: Field,
    mock_lead_fetch_api: MockLeadFetchAPI,
) -> Iterator[MockLeadFetchAPI]:
    """Mock POST."""

    @contextmanager
    def factory() -> None:
        user_response = UserResponse(id=mfield('numeric.increment'))
        with mock_lead_fetch_api(
            method=httpretty.POST,
            body=user_response.json(),
        ):
            yield
    return factory


@pytest.fixture()
@pytest.mark.django_db()
def registered_user(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'UserData',
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
    assert response.url == reverse('identity:login')
    return assert_correct_user(
        registration_data['email'],
        expected_user_data,
    )


@pytest.fixture()
def signin_user_data(
    registration_data: RegistrationData,
    registered_user: User,
) -> SigninUserData:
    """Get registered user signin data."""
    return SigninUserData(
        username=registered_user.email,
        password=registration_data['password1'],
    )


@pytest.fixture()
def expected_user_data(registration_data: RegistrationData) -> UserData:
    """Registration user data without passwords."""
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
@pytest.mark.django_db()
def signedin_user(
    client: Client,
    signin_user_data: SigninUserData,
    registered_user: User,
) -> User:
    """Test successful login."""
    response = client.post(
        reverse('identity:login'),
        data=signin_user_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')

    return registered_user

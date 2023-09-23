import datetime as dt
from typing import Any, Unpack, TYPE_CHECKING
from typing import Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.intrastructure.services.placeholder import UserResponse
from server.apps.identity.models import User

if TYPE_CHECKING:
    from django.test import Client


@final
class UserData(TypedDict, total=False):
    """
    Represent the user data that is required to create a new user.

    Does not include `password`, because it's special field in Django.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    lead_id: int
    is_staff: bool
    is_active: bool


UserAssertion: TypeAlias = Callable[[str, UserData], None]
NotLeadUserAssertion: TypeAlias = Callable[[str], None]


@final
class RegistrationData(UserData, total=False):
    """Represent the user data that is required to create a new user."""

    password_first: str
    password_second: str


@final
class RegistrationDataFactory(Protocol):
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocol."""


@pytest.fixture()
def registration_data_factory() -> RegistrationDataFactory:
    """Fxture that generate fake registration data."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        field = Field(locale=Locale.RU, seed=fields.pop('seed'))
        password = field('password')
        schema = Schema(schema=lambda: {
            'email': field('person.email'),
            'first_name': field('person.first_name'),
            'last_name': field('person.last_name'),
            'date_of_birth': field('datetime.date'),
            'address': field('address.city'),
            'job_title': field('person.occupation'),
            'phone': field('person.telephone'),
        })
        return {
            **schema.create()[0],
            **{'password_first': password, 'password_second': password},
            **fields,
        }

    return factory


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Fixture that check created user attrs from database."""

    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        for field, value_name in expected.items():
            assert getattr(user, field) == value_name

    return factory


@pytest.fixture()
def reg_data(registration_data_factory) -> RegistrationData:
    """Fixture that return user reg data."""
    return registration_data_factory(seed=1)


@pytest.fixture()
def expected_user_data(reg_data: RegistrationData) -> dict[str, Any]:
    """Fixture that return exeected user data."""
    return {
        key: value_name
        for key, value_name in reg_data.items()
        if not key.startswith('password')
    }


@pytest.fixture()
def expected_serialized_user(reg_data: RegistrationData) -> dict[str, Any]:
    """Serialized user's key-values that expected in test."""
    return {
        'name': reg_data['first_name'],
        'last_name': reg_data['last_name'],
        'birthday': reg_data['date_of_birth'].strftime('%d.%m.%Y'),
        'city_of_birth': reg_data['address'],
        'position': reg_data['job_title'],
        'email': reg_data['email'],
        'phone': reg_data['phone'],
    }


@pytest.fixture()
def user(
    expected_user_data: RegistrationData,
) -> 'User':
    """Return created user in database."""
    return User.objects.create(**expected_user_data)


@pytest.fixture()
def expected_user_response(
    expected_user_data: RegistrationData,
) -> 'UserResponse':
    """Return user response obj."""
    return UserResponse(id=1)


@pytest.fixture(scope='session')
def assert_not_lead_user() -> NotLeadUserAssertion:
    """Check that user is not lead."""
    def factory(email: str) -> None:
        user = User.objects.get(email=email)
        assert user.lead_id is None

    return factory


@pytest.fixture()
def authorized_client(client: 'Client', user: 'User') -> 'Client':
    """Authorized User object."""
    client.force_login(user)
    return client

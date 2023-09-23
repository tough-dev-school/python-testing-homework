import datetime as dt
from typing import Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from mimesis import Field, Schema
from typing_extensions import Unpack

from server.apps.identity.models import User


# User Data
class UserData(TypedDict, total=False):
    """Represent the user data."""

    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


@final
class UserDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[UserData]) -> UserData:
        """Create instance of ``UserData`` with overwritten fields."""


@pytest.fixture()
def user_data_factory(field: Field) -> UserDataFactory:
    """Generate random user data."""

    def factory(**fields) -> UserData:
        schema = Schema(
            schema=lambda: {
                'email': field('person.email'),
                'first_name': field('person.first_name'),
                'last_name': field('person.last_name'),
                'date_of_birth': field('datetime.date'),
                'address': field('address.city'),
                'job_title': field('person.occupation'),
                'phone': field('person.telephone'),
            },
            iterations=1,
        )
        return {
            **schema.create()[0],  # type: ignore[misc]
            **fields,
        }

    return factory


# Registration Data
@final
class RegistrationData(UserData, total=False):
    """User data and passwords for registration."""

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """Create instance of ``RegistrationData`` with overwritten fields."""


@pytest.fixture(scope='session')
def registration_data_factory(
    field: Field,
    user_data_factory: UserDataFactory,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = field('password')  # by default passwords are equal
        user_data = user_data_factory()

        return {
            **user_data,
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def user_registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Create instance of ordinary user (not staff or admin)."""
    return registration_data_factory()


@final
class LoginData(TypedDict, total=False):
    """Represent the login data that is required to authenticate a user."""

    username: str
    password: str


UserAssertion: TypeAlias = Callable[[RegistrationData], None]
UserDataExtractor: TypeAlias = Callable[[RegistrationData], UserData]


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Check that user created correctly."""

    def factory(expected: RegistrationData) -> None:
        user = User.objects.get(email=expected['email'])
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            if not field_name.startswith('password'):
                assert getattr(user, field_name) == data_value

    return factory

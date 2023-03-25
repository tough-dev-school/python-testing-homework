import datetime as dt
import random
from typing import Callable, Protocol, TypedDict, final

import pytest
from mimesis import Field, Schema
from mimesis.enums import Locale
from typing_extensions import TypeAlias, Unpack

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data that is required to create a new user.
    It does not include ``password``, because it is very special in django.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str


class UpdateUserData(TypedDict, total=False):
    """
    Represent the simplified user update data that is required to update user.
    It does not include ``password``, because it is very special in django.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str


UserAssertion: TypeAlias = Callable[[str, UserData], None]
UserUpdatedAssertion: TypeAlias = Callable[[str, UpdateUserData], None]


@final
class RegistrationData(UserData, total=False):
    """
    Represent the registration data that is required to create a new user.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


@final
class LoginData(TypedDict, total=False):
    """
    Represent the login data that is required to log an existing user.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    username: str
    password: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        """User data factory protocol."""
        return RegistrationData(**fields)


@final
class LoginDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[LoginData],
    ) -> LoginData:
        """Login data factory protocol."""
        return LoginData(**fields)


@final
class UpdateUserDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[LoginData],
    ) -> UpdateUserData:
        """Update user data factory protocol."""
        return UpdateUserData(**fields)


@pytest.fixture()
def faker_seed():
    return random.seed(10)


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')  # by default passwords are equal
        schema = Schema(
            schema=lambda: {
                'email': mf('person.email'),
                'first_name': mf('person.first_name'),
                'last_name': mf('person.last_name'),
                'date_of_birth': mf('datetime.date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            }
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def login_data_factory(
    faker_seed: int,
) -> LoginDataFactory:
    """Returns factory for fake random data for login."""

    def factory(**fields: Unpack[LoginData]) -> LoginData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'username': mf('person.email'),
                'password': mf('password'),
            }
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory


@pytest.fixture()
def update_user_data_factory(
    faker_seed: int,
) -> UpdateUserDataFactory:
    """Returns factory for fake random data for update user."""

    def factory(**fields: Unpack[UserData]) -> UserData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'first_name': mf('person.first_name'),
                'last_name': mf('person.last_name'),
                'date_of_birth': mf('datetime.date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            }
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture(scope='session')
def assert_user_updated() -> UserUpdatedAssertion:
    """Assert that user updated with correct data."""

    def factory(email: str, expected: UpdateUserData) -> None:
        user = User.objects.get(email=email)
        for field_name, data_value in expected.items():
            if field_name != 'email':
                assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture()
def registration_data(registration_data_factory) -> RegistrationData:
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    typed dist of user data
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def updated_user_data(
    update_user_data_factory: 'UpdateUserDataFactory',
) -> 'UpdateUserData':
    """
    Typed dist with updated data of user
    """
    return update_user_data_factory()


@pytest.fixture()
def db_user(user_data: 'UserDara') -> 'UserData':
    user = User.objects.create(**user_data)
    yield user_data
    user.delete()


@pytest.fixture()
def login_data(
    login_data_factory: LoginDataFactory,
    db_user: UserData,
) -> LoginData:
    return login_data_factory(**{'username': db_user['email'], 'password': 'password'})

from datetime import datetime
from typing import TYPE_CHECKING, Callable, Generator, TypedDict, final

import pytest
from typing_extensions import TypeAlias

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.registration import RegistrationData


UserAssertion: TypeAlias = Callable[[str, 'UserData'], None]
UserGenerator: TypeAlias = Generator['UserData', User, None]


@final
class UserData(TypedDict, total=False):
    """
    Represent the user data that is required to create a new user.
    It does not include ``password``, because it is very special in django.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    """
    Represent the registration data that is required to create a new user.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """
    password1: str
    password2: str


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> UserData:
    """
    We need to simplify registration data to drop passwords.
    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def create_user(db, user_data: UserData) -> User:
    """Returns user object with fake random data added to the database."""
    return User.objects.create(**user_data)


@pytest.fixture()
def get_user(user_data: UserData) -> UserGenerator:
    """Generator user object from database."""
    user = User.objects.create(**user_data)
    yield user
    user.delete()


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Checking the correctness of the data of the created user."""

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

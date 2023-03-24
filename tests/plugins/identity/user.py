from datetime import datetime
from typing import Callable, Generator, TypedDict, final

import pytest
from django.test import Client
from mimesis.locales import Locale
from mimesis.schema import Field
from typing_extensions import TypeAlias

from server.apps.identity.models import User

UserAssertion: TypeAlias = Callable[[str, 'UserData'], None]
UserGenerator: TypeAlias = Generator['UserData', User, None]
UserExternalAssertion: TypeAlias = Callable[
    ['ExternalAPIUserResponse', 'UserData'],
    None,
]


@final
class UserData(TypedDict, total=False):
    """Represent the user data that is required to create a new user.

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
    """Represent the registration data that is required to create a new user.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


class ExternalAPIUserResponse(UserData, total=False):
    """User data in external JSON Server.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    id: int


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def expected_user_data(user_data: 'UserData') -> 'UserData':
    """Represent the user data without password."""
    return user_data


@pytest.fixture()
def create_user(db, user_data: UserData) -> User:
    """Returns user object with fake random data added to the database."""
    return User.objects.create(**user_data)


@pytest.fixture()
def get_user(db, user_data: UserData) -> UserGenerator:
    """Generator user object from database."""
    user = User.objects.create(**user_data)
    yield user
    user.delete()


@pytest.fixture()
def _unauthorized_client(request: pytest.FixtureRequest) -> None:
    """Injecting Django test unauthorized Client into the class."""
    request.cls.client = Client()


@pytest.fixture()
def _generate_credentials(
    request: pytest.FixtureRequest,
    faker_seed: int,
) -> None:
    """Generating random credentials."""
    field = Field(locale=Locale.EN, seed=faker_seed)
    request.cls.username = field('email')
    request.cls.password = field('password')


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


@pytest.fixture(scope='session')
def assert_correct_external_user() -> UserExternalAssertion:
    """Assert that user data in external API is the same as expected one."""

    def factory(
        external_api_user_response: ExternalAPIUserResponse,
        expected: UserData,
    ) -> None:
        assert external_api_user_response['id']
        for field, field_value in expected.items():
            if field == User.USER_DATE_OF_BIRTH_FIELD:
                field_value = str(field_value)
            assert external_api_user_response[field] == field_value

    return factory

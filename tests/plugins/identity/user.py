import datetime as dt
from typing import Callable, Protocol, TypeAlias, TypedDict, Unpack, cast, final

import pytest
from mimesis import BaseProvider, Field, Locale
from mimesis.schema import Schema

from server.apps.identity.models import User

UserAssertion: TypeAlias = Callable[[str, 'UserData'], None]


class FakeProvider(BaseProvider):
    """Represents a fake test data provider."""

    class Meta:  # noqa: WPS306
        name = 'FakeProvider'

    def random_seed(self) -> int:
        """Generate random seed."""
        return self.random.randint(0, 100)

    def user_factory(
        self,
        **fields: Unpack['RegistrationData'],
    ) -> 'RegistrationData':
        """Factory for generating user data used during registration."""
        mf = Field(locale=Locale.RU, seed=self.random_seed())
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
            },
        )
        return {
            **schema.create()[0],  # type: ignore[typeddict-item]
            **{'password1': password, 'password2': password},
            **fields,
        }


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


@final
class RegistrationData(UserData, total=False):
    """
    Represent the registration data that is required to create a new user.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


class RegistrationDataFactory(Protocol):
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """Must implement in logic."""


@pytest.fixture()
def expected_user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return cast(
        UserData,
        {
            key_name: value_part
            for key_name, value_part in registration_data.items()
            if not key_name.startswith('password')
        },
    )


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Returns fake random data for registration."""
    return registration_data_factory()


@pytest.fixture()
def registration_data_factory() -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""
    return FakeProvider().user_factory


@pytest.fixture()
def create_user(expected_user_data: UserData) -> User:
    """Create a user."""
    return User.objects.create(**expected_user_data)


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Asserts that user with the given email exists and has expected data."""

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

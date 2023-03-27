from datetime import datetime
from typing import TYPE_CHECKING, Callable, Protocol, TypedDict, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import TypeAlias, Unpack

from server.apps.identity.models import User

if TYPE_CHECKING:
    from django.test import Client


UserAssertion: TypeAlias = Callable[[str, 'UserData'], None]


class UserData(TypedDict, total=False):
    """Represent the simplified user data that is required to create a new user.

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


class RegistrationDataFactory(Protocol):
    """Annotations for RegistrationData factory."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocol."""


@pytest.fixture()
def registration_data_factory(faker_seed: int) -> 'RegistrationDataFactory':
    """Returns factory for fake random data for regitration."""

    def factory(**fields: Unpack['RegistrationData']) -> 'RegistrationData':
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')  # by default passwords are equal
        schema = Schema(schema=lambda: {
            'email': mf('person.email'),
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf('datetime.date'),
            'address': mf('address.city'),
            'job_title': mf('person.occupation'),
            'phone': mf('person.telephone'),
        })
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }
    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: 'RegistrationDataFactory',
) -> 'RegistrationData':
    """Returns random registration data."""
    return registration_data_factory()


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Assert correct user creation."""
    def factory(email: str, expected: 'UserData') -> None:
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


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture(scope='session')
def mimesis_field(faker_seed: int) -> Field:
    """Returns mimesis field with random seed."""
    return Field(locale=Locale.RU, seed=faker_seed)


@pytest.fixture()
def user(
    mimesis_field: Field,
    user_data: UserData,
    django_user_model: User,
) -> 'User':
    """Returns app user."""
    fields = dict(user_data)
    fields['password'] = mimesis_field('password')

    return django_user_model.objects.create(**fields)


@pytest.fixture()
def user_client(user: 'User', client: 'Client') -> 'Client':
    """Returns logged in client."""
    client.force_login(user)

    return client

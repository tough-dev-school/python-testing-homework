import datetime as dt
import json
import random
from typing import (Callable, final, Protocol, TypedDict, Generator)

import httpretty
import pytest
from django.conf import settings
from django.test import Client
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Unpack, TypeAlias

from server.apps.identity.models import User
from tests.plugins.constants import URL_HTTPRETTY_FINAL, SEED_LENGTH_IN_BITS


def faker_random_seed() -> int:
    """Generate random number."""
    return random.Random().getrandbits(SEED_LENGTH_IN_BITS)


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


@final
class RegistrationDataFactory(Protocol):
    """Factory for registration data."""

    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        """User data factory protocol."""


def _factory(
    faker_seed: Callable[[None], int],
) -> Callable[[Unpack[RegistrationData]], RegistrationData]:
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
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
def registration_random_data_factory(
) -> RegistrationDataFactory:
    """Return factory for creating random mimesis schema."""
    return _factory(faker_random_seed)


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> RegistrationDataFactory:
    """Return factory for creating mimesis schema."""
    return _factory(faker_seed)


@pytest.fixture()
def user_data(
    registration_data_factory: 'RegistrationDataFactory',
) -> 'UserData':
    """Fixture for getting user data."""
    registration_data = registration_data_factory()
    user_registration_data = {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }
    user_registration_data['password'] = registration_data['password1']
    return user_registration_data


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.mark.django_db()
@pytest.fixture()
def user_registration(
    client: Client,
    user_data: 'UserData',
) -> Generator[User, None, None]:
    """User registration fixture."""
    user = User.objects.create(**user_data)
    client.force_login(user)
    yield user
    User.objects.filter(email=user.email).delete()


@httpretty.activate
@pytest.fixture()
def mock_user_service() -> None:
    """Mock DJANGO_PLACEHOLDER_API_URL using httpretty."""

    def factory(body_object: any) -> None:
        settings.PLACEHOLDER_API_URL = URL_HTTPRETTY_FINAL
        httpretty.register_uri(
            httpretty.GET,
            '{0}users'.format(URL_HTTPRETTY_FINAL),
            body=json.dumps(body_object),
        )

    httpretty.enable(verbose=True, allow_net_connect=False)
    yield factory, 1
    httpretty.reset()

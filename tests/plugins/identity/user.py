import datetime as dt
from typing import (Callable, final, Protocol, TypedDict, Generator, Tuple)

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from typing_extensions import Unpack, TypeAlias
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

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
    phone_type: int


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


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> RegistrationDataFactory:
    """Return factory for creating mimesis schema."""

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
            'phone_type': mf('choice', items=[1, 2, 3]),
        })
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """Fixture for getting user data."""
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.mark.django_db()
@pytest.fixture()
def user_registration(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> Generator[Tuple['UserData', HttpResponse], None, None]:
    """User registration fixture."""
    post_data = registration_data_factory()
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    yield post_data, response
    User.objects.filter(email=post_data['email']).delete()

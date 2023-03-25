from datetime import datetime
from typing import Protocol, TypedDict, final

import pytest
from mimesis.schema import Field, Schema
from typing_extensions import Unpack


class UserData(TypedDict, total=False):
    """
    Simplified user data that is required to create a new user.

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
    Registration data that is required to create a new user.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """Return registration data on call."""


@pytest.fixture()
def registration_data_factory(fake_field: Field) -> RegistrationDataFactory:
    """Factory for fake random data for registration."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = fake_field('password')  # by default passwords are equal
        schema = Schema(
            schema=lambda: {
                'email': fake_field('person.email'),
                'first_name': fake_field('person.first_name'),
                'last_name': fake_field('person.last_name'),
                'date_of_birth': fake_field('datetime.date'),
                'address': fake_field('address.city'),
                'job_title': fake_field('person.occupation'),
                'phone': fake_field('person.telephone'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory

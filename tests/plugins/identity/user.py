import datetime as dt
from typing import Callable, Protocol, TypeAlias, TypedDict, Unpack, final

import pytest
from mimesis import Field, Locale, Schema

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data that is required to create a new user.

    It does not include ``password``, because it is very special in django.
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
    """Represent the registration data that is required to create a new user."""

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """Method to call as a function with RegistrationData as kwargs."""


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture()
def registration_data_factory(faker_seed: int) -> RegistrationDataFactory:
    """Returns factory for random data generation."""
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')
        schema = Schema(
            schema=lambda: {
                'email': mf('person:email'),
                'first_name': mf('person:first_name'),
                'last_name': mf('person:last_name'),
                'date_of_birth': mf('datetime:date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            }, iterations=1,
        )
        return {
            **schema.create()[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Returns fake random data for regitration."""
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """
    We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Factory to compare all user fields."""
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory

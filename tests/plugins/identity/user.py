from typing import Protocol, TypedDict, Unpack, final
import pytest
import datetime as dt
from mimesis.locales import Locale
from mimesis.schema import Field, Schema


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
    def __call__(self, **fields: Unpack[RegistrationData],) -> RegistrationData:
        """User data factory protocol."""


@pytest.fixture()
def registration_data(registration_data_factory: RegistrationDataFactory,) -> RegistrationData:
    """Returns fake random data for regitration."""
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """
    We need to simplify registration data to drop passwords.
    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return { # type: ignore[return-value]
    key_name: value_part
    for key_name, value_part in registration_data.items()
    if not key_name.startswith('password')
    }


@pytest.fixture()
def registration_data_factory(faker_seed: int,) -> RegistrationDataFactory:
    """Returns factory for fake random data for regitration."""
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password') # by default passwords are equal
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
        **schema.create(iterations=1)[0], # type: ignore[misc]
        **{'password1': password, 'password2': password},
        **fields,
        }
    return factory

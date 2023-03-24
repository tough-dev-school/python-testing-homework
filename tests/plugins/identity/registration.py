from typing import TYPE_CHECKING, Protocol, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

if TYPE_CHECKING:
    from plugins.identity.user import RegistrationData


@final
class RegistrationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack['RegistrationData'],
    ) -> 'RegistrationData':
        """User registration data factory protocol."""


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""

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
            'phone': mf('person.telephone')
        })
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> 'RegistrationData':
    """
    Returns fake random user data for user registration.
    """
    return registration_data_factory()

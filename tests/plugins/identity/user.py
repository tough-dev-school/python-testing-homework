import pytest

from typing import final, TypedDict
from typing_extensions import Protocol, Unpack
from mimesis.locales import Locale
from mimesis.schema import Field, Schema


class UserDetails(TypedDict, total=False):
    """User details data."""

    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@final
class UserRegisterDetails(TypedDict, total=False):
    """User registration details data."""

    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str
    email: str
    password1: str
    password2: str


@final
class UserDetailsFactory(Protocol):  # type: ignore[misc]
    """A factory to generate `UserDetails`."""

    def __call__(
        self,
        **fields: Unpack[UserDetails],
    ) -> UserDetails:
        """User profile details factory protocol."""


@final
class UserRegisterDetailsFactory(Protocol):  # type: ignore[misc]
    """A factory to generate `UserRegisterDetails`."""

    def __call__(
        self,
        **fields: Unpack[UserRegisterDetails],
    ) -> UserRegisterDetails:
        """User registration details factory protocol."""


@pytest.fixture()
def user_details_factory(
    faker_seed: int,
) -> UserDetailsFactory:
    def factory(
        **fields: Unpack[UserDetails],
    ) -> UserDetails:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(schema=lambda: {
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf(
                'datetime.formatted_date',
                fmt='%Y-%m-%d',
            ),
            'address': mf('address.address'),
            'job_title': mf('person.occupation'),
            'phone': mf('person.telephone'),
        })
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }
    return factory


@pytest.fixture()
def user_register_details_factory(
    user_details_factory: UserDetailsFactory,
    faker_seed: int,
) -> UserRegisterDetailsFactory:
    def factory(
        **fields: Unpack[UserRegisterDetails],
    ) -> UserRegisterDetails:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')
        email = mf('person.email'),
        return {
            **user_details_factory(),  # type: ignore[misc]
            **{
                'email': email,
                'password1': password,
                'password2': password,
            },
            **fields,
        }
    return factory

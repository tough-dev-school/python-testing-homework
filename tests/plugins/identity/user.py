from collections.abc import Callable
from typing import TypedDict, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Protocol, TypeAlias, Unpack

from server.apps.identity.models import User

BIRTH_DATE_FORMAT = '%Y-%m-%d'  # noqa: WPS323


class UserDetails(TypedDict, total=False):
    """User details data."""

    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@final
class UserRegisterDetails(UserDetails, total=False):
    """User registration details data."""

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
    """User profile details factory."""
    def factory(
        **fields: Unpack[UserDetails],
    ) -> UserDetails:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(schema=lambda: {
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf(
                'datetime.formatted_date',
                fmt=BIRTH_DATE_FORMAT,
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
def user_details(
    user_details_factory: UserDetailsFactory,
) -> UserDetails:
    """User profile details."""
    return user_details_factory()


@pytest.fixture()
def user_register_details_factory(
    user_details: UserDetails,
    faker_seed: int,
) -> UserRegisterDetailsFactory:
    """User registration details factory."""
    def factory(
        **fields: Unpack[UserRegisterDetails],
    ) -> UserRegisterDetails:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')
        email = mf('person.email')
        return {
            **user_details,  # type: ignore[misc]
            **{
                'email': email,
                'password1': password,
                'password2': password,
            },
            **fields,
        }
    return factory


@pytest.fixture()
def user_register_details(
    user_register_details_factory: UserRegisterDetailsFactory,
) -> UserRegisterDetails:
    """User registration details."""
    return user_register_details_factory()


UserDetailsAssertion: TypeAlias = Callable[[str, UserDetails], None]


@pytest.fixture(scope='session')
def assert_user_details() -> UserDetailsAssertion:
    """User details assertion."""
    def factory(email: str, expected: UserDetails) -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # date fields:
        assert user.date_of_birth
        assert user.date_of_birth.isoformat() == expected.pop('date_of_birth')
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value
    return factory


@pytest.fixture(
    params=[
        'invalid',
        'invalid@',
        'invalid@invalid',
        'invalid@invalid.',
        'someone@somewhere@invalid',
    ],
)
def invalid_email(request) -> str:
    """Invalid email."""
    return request.param

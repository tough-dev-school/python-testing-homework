"""Identity data related plugins."""
from datetime import datetime
from typing import Callable, Protocol, TypeAlias, TypedDict, Unpack, final

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.auth.models import User
from mimesis.locales import Locale
from mimesis.schema import Field, Schema


@final
class ProfileData(TypedDict, total=False):
    """Represent the simplified profile data."""

    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str


ProfileAssertion: TypeAlias = Callable[[str, ProfileData], None]


class ProfileDataFactory(Protocol):
    """Factory for representation of the simplified profile data."""

    def __call__(self, **fields: Unpack[ProfileData]) -> ProfileData:
        """User data factory protocol."""


@pytest.fixture()
def profile_data_factory(
    faker_seed: int,
) -> ProfileDataFactory:
    """Returns factory for fake random profile data."""

    def factory(**fields: Unpack[ProfileData]) -> ProfileData:
        mf = Field(locale=Locale.EN, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'first_name': mf('person.first_name'),
                'last_name': mf('person.last_name'),
                'date_of_birth': mf('datetime.date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            },
            iterations=1,
        )
        return {
            **schema.create()[0],  # type: ignore[typeddict-item]
            **fields,
        }

    return factory


@pytest.fixture(scope='session')
def assert_correct_profile() -> ProfileAssertion:
    """All profile fields are equal to reference."""

    def factory(email: str, expected: ProfileData) -> None:
        user = get_user_model().objects.get(email=email)
        assert user.id
        assert user.is_active
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value
    return factory


@pytest.fixture(scope='session')
def assert_incorrect_profile() -> ProfileAssertion:
    """At least one field does not match."""

    def factory(email: str, expected: ProfileData) -> None:
        user = get_user_model().objects.get(email=email)
        assert user.id
        assert user.is_active
        matches = []
        for field_name, data_value in expected.items():
            matches.append(getattr(user, field_name) == data_value)

        assert not all(matches)

    return factory


@pytest.fixture(scope='function')
def logged_user_client(client: Client, django_user_model: User):
    """Client for a logged in user."""
    password, email = 'password', 'email@example.com'
    user = django_user_model.objects.create_user(
        email,
        password,
    )
    client.force_login(user)
    return client

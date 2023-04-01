from typing import Any, Callable, Generator

import pytest
from django.test import Client
from typing_extensions import TypeAlias

from server.apps.identity.models import User
from tests.plugins.identity.registration import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)

FieldMissingAssertion: TypeAlias = Callable[[Any], None]


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Registration data with all required fields."""
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


@pytest.fixture()
def db_user(user_data: UserData) -> Generator[User, None, None]:
    """Created user model in database."""
    user = User.objects.create(**user_data)
    yield user
    user.delete()


@pytest.fixture()
def client_logined(
    client: Client,
    db_user: User,
) -> Generator[Client, None, None]:
    """Client with simulated user login."""
    client.force_login(user=db_user)
    yield client
    client.logout()


@pytest.fixture(scope='session')
def assert_field_missing() -> FieldMissingAssertion:
    """Assert that response content implies that required field is missing."""

    def factory(resp_content: Any) -> None:
        assert b'required' in resp_content

    return factory

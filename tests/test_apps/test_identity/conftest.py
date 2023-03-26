from typing import Any, Callable, Generator

import pytest
from typing_extensions import TypeAlias

from server.apps.identity.models import User
from tests.plugins.identity.registration import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)
from tests.plugins.identity.user_update import UserUpdateData

UserAssertion: TypeAlias = Callable[[str, UserUpdateData], None]
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


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Assert that db user data is the same as expected one."""

    def factory(email: str, expected: UserUpdateData) -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            # Date_of_birth is None in User DB model
            if field_name == User.DATE_OF_BIRTH_FIELD and not data_value:
                data_value = None  # noqa: WPS 440
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture(scope='session')
def assert_field_missing() -> FieldMissingAssertion:
    """Assert that response content implies that required field is missing."""

    def factory(resp_content: Any) -> None:
        assert b'required' in resp_content

    return factory

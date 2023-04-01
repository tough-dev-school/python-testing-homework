from typing import Callable

import pytest
from typing_extensions import TypeAlias

from server.apps.identity.models import User
from tests.plugins.identity.user_update import UserUpdateData

UserAssertion: TypeAlias = Callable[[str, UserUpdateData], None]


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

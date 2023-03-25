from typing import TYPE_CHECKING

import pytest

from server.apps.identity.models import User

if TYPE_CHECKING:
    from protocols.identity.user import UserDict


@pytest.fixture()
def assert_correct_user():
    """Assert stmts for user instance."""
    def factory(email: str, expected: 'UserDict'):
        """Asserts function."""
        user = User.objects.get(email=email)
        assert user.email == expected['email']
        assert user.job_title == expected['job_title']
        assert user.address == expected['address']
        assert user.last_name == expected['last_name']
        assert user.first_name == expected['first_name']
        assert user.date_of_birth == expected['date_of_birth']

    return factory


@pytest.fixture()
def assert_correct_update_user():
    """Assert stmts for updated user instance."""
    def factory(user_before: User, expected: 'UserDict'):
        """Asserts function."""
        user = User.objects.get(email=user_before.email)

        assert user.email == expected['email']
        assert user.job_title == expected['job_title']
        assert user.address == expected['address']
        assert user.last_name == expected['last_name']
        assert user.first_name == expected['first_name']
        assert user.date_of_birth == expected['date_of_birth']

    return factory

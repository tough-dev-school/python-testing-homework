from typing import Any

import pytest

from server.apps.identity.models import _UserManager


class TestUserManager:
    """Test class for testing _UserManager."""

    @pytest.mark.django_db()
    def test_create_user(
        self,
        reg_data,
        expected_user_data: dict[str, Any],
        assert_correct_user,
    ) -> None:
        """Testing create_user method in _UserManager."""
        _UserManager().create_user(
            password=reg_data['password_first'],
            **expected_user_data,
        )
        assert_correct_user(reg_data['email'], expected_user_data)

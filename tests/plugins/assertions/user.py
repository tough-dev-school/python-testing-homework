from http import HTTPStatus
from typing import Callable

import pytest
from typing_extensions import TypeAlias

from server.apps.identity.models import User
from tests.plugins.identity.user import UserData

UserAssertion: TypeAlias = Callable[[str, "UserData"], None]
UserAssertionNegative: TypeAlias = Callable[[HTTPStatus, str], None]


@pytest.fixture()
def assert_correct_user() -> UserAssertion:
    def assert_fun(user_email: str, expected_data: "UserData") -> None:
        user = User.objects.get(email=user_email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in expected_data.items():
            assert getattr(user, field_name) == data_value

    return assert_fun


@pytest.fixture()
def assert_user_not_registered() -> UserAssertionNegative:
    def assert_fun(response_status_code: HTTPStatus, user_email: str) -> None:
        assert response_status_code == HTTPStatus.OK
        assert not User.objects.filter(email=user_email)

    return assert_fun

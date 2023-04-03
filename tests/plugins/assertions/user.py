from http import HTTPStatus

import pytest

from server.apps.identity.models import User


@pytest.fixture()
def assert_correct_user():
    def assert_fun(user_email, expected_data):
        user = User.objects.get(email=user_email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        
        for field_name, data_value in expected_data.items():
            assert getattr(user, field_name) == data_value

    return assert_fun


@pytest.fixture()
def assert_user_not_registered():
    def assert_fun(response_status_code, user_email):
        assert response_status_code == HTTPStatus.OK
        assert not User.objects.filter(email=user_email)

    return assert_fun

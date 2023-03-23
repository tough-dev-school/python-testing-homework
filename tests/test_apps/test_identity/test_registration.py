from http import HTTPStatus
from typing import Any, Callable, Mapping

from django.test import Client
import pytest

from server.apps.identity.models import User


@pytest.mark.django_db
def test_success(
    client: Client,
    user_email: str,
    user_password: str,
    user_profile_data: Mapping[str, Any],
    assert_user_profile: Callable[[User, Mapping[str, Any]], None],
) -> None:
    auth_data = {
        'email': user_email,
        'password1': user_password,
        'password2': user_password,
    }
    response = client.post(
        '/identity/registration',
        data=auth_data | user_profile_data,
    )
    assert response.status_code == HTTPStatus.FOUND, (
        response.context['form'].errors
    )
    user = User.objects.all().get(email=user_email)
    assert user.check_password(user_password)
    assert_user_profile(user, user_profile_data)

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.test import Client
import pytest

from server.apps.identity.models import User


if TYPE_CHECKING:
    from tests.plugins.identity.user import ProfileData, ProfileAssertion


@pytest.mark.django_db
def test_success(
    client: Client,
    user_email: str,
    user_password: str,
    user_profile_data: 'ProfileData',
    assert_user_profile: 'ProfileAssertion',
) -> None:
    auth_data = {
        'email': user_email,
        'password1': user_password,
        'password2': user_password,
    }
    response = client.post(
        '/identity/registration',
        data=user_profile_data | auth_data,
    )
    assert response.status_code == HTTPStatus.FOUND, (
        response.context['form'].errors
    )
    user = User.objects.all().get(email=user_email)
    assert user.check_password(user_password)
    assert_user_profile(user, user_profile_data)

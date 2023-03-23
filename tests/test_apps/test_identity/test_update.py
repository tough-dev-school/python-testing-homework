from http import HTTPStatus
from typing import TYPE_CHECKING

from django.test import Client
import pytest

from server.apps.identity.models import User


if TYPE_CHECKING:
    from tests.plugins.identity.user import ProfileData, ProfileAssertion


@pytest.mark.django_db
def test_valid_update(
    admin_client: Client,
    admin_user: User,
    user_profile_data: 'ProfileData',
    assert_user_profile: 'ProfileAssertion',
) -> None:
    response = admin_client.post(
        '/identity/update',
        data=user_profile_data,
    )
    assert response.status_code == HTTPStatus.FOUND, (
        response.context['form'].errors
    )
    admin_user.refresh_from_db()
    assert_user_profile(admin_user, user_profile_data)

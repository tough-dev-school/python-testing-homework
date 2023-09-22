from http import HTTPStatus

import pytest
from django.urls import reverse

from server.apps.identity.models import User


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user_data_for_registration(user) -> dict:
    user.last_login = ""
    user.lead_id = ""
    return user.__dict__


def test_success_registration(
    client,
    user_data_for_registration,
):
    response = client.post(
        reverse('identity:registration'),
        data=user_data_for_registration,
    )

    assert response.status_code == HTTPStatus.OK
    assert User.objects.get(email=user_data_for_registration['email']) is not None

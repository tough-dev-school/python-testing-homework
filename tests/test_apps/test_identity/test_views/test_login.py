import pytest

from typing import TYPE_CHECKING

from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client
    from tests.plugins.identity.user import UserRegisterDetailsFactory

pytestmark = [
    pytest.mark.django_db,
]


def test_register(
    client: 'Client',
    user_register_details_factory: 'UserRegisterDetailsFactory',
):
    response = client.post(
        reverse('identity:registration'),
        data=user_register_details_factory(),
    )

    assert response.status_code == 302
    assert response['Location'] == reverse('identity:login')

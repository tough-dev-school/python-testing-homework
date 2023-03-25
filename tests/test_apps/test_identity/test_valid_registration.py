from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        UserAssertion,
        UserData,
    )

@pytest.mark.django_db()
def test_valid_registration(
        client: Client,
        registration_data: 'RegistrationData',
        expected_user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], expected_user_data)
    assert True

from http import HTTPStatus

import pytest
from django.test.client import Client
from plugins.identity.user import RegistrationData, UserAssertion, UserData


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: RegistrationData,
    user_data: UserData,
    assert_correct_user: UserAssertion,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post('/identity/registration', data=registration_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == '/identity/login'
    assert_correct_user(registration_data['email'], user_data)

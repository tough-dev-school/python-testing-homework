import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model


from ...plugins.identity.user import (
    RegistrationData,
    UserAssertion,
    UserData,
)


# User = get_user_model()

# @pytest.mark.django_db()
# def test_valid_registration(client: Client) -> None:
#     registration_data = {
#         'email': 'mail@sobolevn.me',
#         'first_name': 'Nikita',
#         'last_name': 'Sobolev',
#         'date_of_birth': '01.01.2023',
#         'address': 'City',
#         'job_title': 'CTO',
#         'phone': '+7985000',
#         'password1': 'password1',
#         'password2': 'password1'
#     }
#     response = client.post(
#         reverse('identity:registration'),
#         data=registration_data,
#     )
#     assert response.status_code == HTTPStatus.FOUND
#     assert response.get('Location') == reverse('identity:login')
#     user = User.objects.get(email=registration_data['email'])
#     assert user.id
#     assert user.is_active
#     assert not user.is_superuser
#     assert not user.is_staff
#     assert user.first_name == registration_data['first_name']
#     assert user.last_name == registration_data['last_name']
#     assert user.job_title == registration_data['job_title']


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

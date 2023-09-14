from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from django.urls import reverse


@pytest.mark.django_db()
def test_user_can_login(client, mock_user_data, mock_registration_data, mock_user_create_api, assert_correct_user):
    """Test new user is can register"""
    response = client.post(
        reverse('identity:registration'),
        data=urlencode(mock_registration_data),
        content_type="application/x-www-form-urlencoded")

    assert response.status_code == HTTPStatus.FOUND
    assert_correct_user(mock_registration_data['email'], {
        **mock_user_data,
        'lead_id': mock_user_create_api['id']
    })

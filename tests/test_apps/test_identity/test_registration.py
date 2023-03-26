from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from server.apps.identity.models import User
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationDataFactory,
        RegistrationData,
        UserAssertion,
        UserData,
    )

@pytest.mark.django_db()
def test_valid_registration(
        client: Client,
        registration_data: 'RegistrationData',
        user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], user_data)
    assert True


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(
        **{field: ''},  # type: ignore[arg-type]
    )
    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email']).exists()

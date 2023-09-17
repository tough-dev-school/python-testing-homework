from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


def test_registration_page_exists(client: Client) -> None:
    response = client.get(reverse('identity:registration'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_registration_success(
    client: Client,
    valid_registration_data: 'RegistrationData',
    valid_user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration is successfully with valid registration data."""
    response = client.post(
        reverse('identity:registration'),
        data=valid_registration_data
    )

    assert response.status_code == HTTPStatus.OK
    assert_correct_user(valid_registration_data['email'], valid_user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    post_data = registration_data_factory(
        **{field: ''},  # type: ignore[arg-type]
    )

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])

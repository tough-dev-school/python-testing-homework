from http import HTTPStatus
from typing import TYPE_CHECKING, Tuple

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import RegistrationDataFactory, UserData


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
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_success_registration(
    user_registration: Tuple['UserData', HttpResponse],
) -> None:
    """Test that missing required will fail the registration."""
    post_data, response = user_registration
    assert response.status_code == HTTPStatus.FOUND
    assert User.objects.filter(email=post_data['email'])

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.pytest_identity import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


def expected_new_user_data(registration_data: 'RegistrationData') -> 'UserData':
    """Registration user data without passwords."""
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.mark.django_db()
def test_user_succesful_update(
    client: Client,
    signedin_user: User,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Update works with correct user data."""
    update_user_data = registration_data_factory(
        # Everything new, except email
        email=signedin_user.email,
    )
    response = client.post(
        reverse('identity:user_update'),
        data=update_user_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:user_update')
    assert_correct_user(signedin_user.email, expected_new_user_data(update_user_data))

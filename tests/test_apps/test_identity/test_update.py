from contextlib import contextmanager
from http import HTTPStatus
from typing import TYPE_CHECKING, Iterator

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.identity import MockLeadFetchAPI
    from tests.plugins.identity.pytest_identity import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


def expected_user_data(registration_data: 'RegistrationData') -> 'UserData':
    """Registration user data without passwords."""
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def mock_lead_patch_user_api(
    mfield: Field,
    mock_lead_fetch_api: 'MockLeadFetchAPI',
) -> Iterator['MockLeadFetchAPI']:
    """Mock PATCH request."""
    @contextmanager
    def factory() -> None:
        user_response = UserResponse(id=mfield('numeric.increment'))
        with mock_lead_fetch_api(method='PATCH', body=user_response.json()):
            yield
    return factory


@pytest.mark.django_db()
def test_user_succesful_update(
    client: Client,
    signedin_user: User,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
    mock_lead_patch_user_api: 'MockLeadFetchAPI',
) -> None:
    """Update works with correct user data."""
    update_user_data = registration_data_factory(
        # Everything new, except email
        email=signedin_user.email,
    )
    with mock_lead_patch_user_api():
        response = client.post(
            reverse('identity:user_update'),
            data=update_user_data,
        )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:user_update')
    assert_correct_user(
        signedin_user.email,
        expected_user_data(update_user_data),
    )

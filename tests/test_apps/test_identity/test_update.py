from contextlib import contextmanager
from http import HTTPStatus
from typing import TYPE_CHECKING, Callable, Iterator

try:
    # Requires Python 3.10
    from typing import TypeAlias  # noqa: WPS433 # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias  # noqa: WPS433, WPS440

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
        ExpectedUserData,
        RegistrationDataFactory,
        UserAssertion,
    )


MockPatchLeadFetchAPI: TypeAlias = Callable[[], None]


@pytest.fixture()
def mock_lead_patch_user_api(
    mfield: Field,
    mock_lead_fetch_api: MockPatchLeadFetchAPI,
) -> Iterator[MockPatchLeadFetchAPI]:
    """Mock PATCH request."""
    @contextmanager
    def factory() -> Iterator[None]:
        user_response = UserResponse(id=mfield('numeric.increment'))
        with mock_lead_fetch_api(method='PATCH', body=user_response.json()):
            yield
    return factory


@pytest.mark.django_db()
def test_user_succesful_update(  # noqa: WPS211
    client: Client,
    signedin_user: User,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
    mock_lead_patch_user_api: 'MockLeadFetchAPI',
    expected_user_data: 'ExpectedUserData',
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
    assert response.url == reverse('identity:user_update')  # type: ignore[attr-defined]
    assert_correct_user(
        signedin_user.email,
        expected_user_data(update_user_data),
    )

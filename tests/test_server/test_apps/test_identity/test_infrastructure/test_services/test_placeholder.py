# isort: skip_file
# flake8: noqa
from typing import Any

import pytest
from pydantic import ValidationError

from server.apps.identity.intrastructure.services.placeholder import (
    LeadCreate,
    LeadUpdate,
    UserResponse,
    _serialize_user,
)
from server.apps.identity.models import User
from server.common.django.types import Settings
from tests.plugins.identity.user import RegistrationData, UserAssertion


@pytest.mark.django_db()
def test_success_lead_create(
    user: User,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
    assert_correct_user: UserAssertion,
    settings: Settings,
) -> None:
    """Testing service that create lead user."""
    assert_correct_user(reg_data['email'], expected_user_data)
    actual_id = 11
    actual_response = UserResponse(id=actual_id)
    expected_id = LeadCreate(
        api_timeout=settings.PLACEHOLDER_API_TIMEOUT,
        api_url=settings.PLACEHOLDER_API_URL,
    )(user=user)
    assert actual_response.id == expected_id


def test_success_url_path(settings: Settings) -> None:
    """Testing method that create URL path for the request."""
    expected_url_path = 'https://jsonplaceholder.typicode.com/users'
    fetcher = LeadCreate(
        api_timeout=settings.PLACEHOLDER_API_TIMEOUT,
        api_url=settings.PLACEHOLDER_API_URL,
    )
    actual_url_path = fetcher.url_path()
    assert actual_url_path == expected_url_path


@pytest.mark.django_db()
def test_success_lead_update(
    user: User,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
    assert_correct_user: UserAssertion,
    settings: Settings,
) -> None:
    """Testing service that update lead user."""
    assert_correct_user(reg_data['email'], expected_user_data)
    LeadUpdate(
        api_timeout=settings.PLACEHOLDER_API_TIMEOUT,
        api_url=settings.PLACEHOLDER_API_URL,
    )(user=user)


def test_success_validate_user_response() -> None:
    """Testing UserResponse model, success case."""
    expected_id = 1
    actual_id = UserResponse.model_validate({'id': 1}).id
    assert actual_id == expected_id


def test_failed_validate_user_response() -> None:
    """Testing UserResponse model, failed case."""
    with pytest.raises(ValidationError) as exc:
        UserResponse.model_validate({'TEST': 1}).id  # noqa: WPS428
    assert 'ValidationError' in exc.typename  # noqa: WPS441


@pytest.mark.django_db()
def test_success_serialize_user(
    user: User,
    expected_serialized_user: dict[str, Any],
) -> None:
    """Testing _serialize_user function."""
    actial_serialization = _serialize_user(user=user)
    assert actial_serialization == expected_serialized_user

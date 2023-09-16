from typing import Any

import pytest
from pydantic import ValidationError

from conftest import user
from protocols import UserAssertion, RegistrationData
from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
    LeadCreate,
    LeadUpdate,
    _serialize_user,
)
from server.apps.identity.models import User

API_URL = "https://jsonplaceholder.typicode.com/"
API_TIMEOUT = 3


@pytest.mark.django_db
def test_success_lead_create(
    user: User,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
    assert_correct_user: UserAssertion,
) -> None:
    assert_correct_user(reg_data["email"], expected_user_data)
    actual_id = UserResponse(id=11)
    expected_id = LeadCreate(api_timeout=API_TIMEOUT, api_url=API_URL)(user=user)
    assert actual_id == expected_id


@pytest.mark.django_db
def test_success_lead_update(
    user: User,
    reg_data: RegistrationData,
    expected_user_data: dict[str, Any],
    assert_correct_user: UserAssertion,
) -> None:
    assert_correct_user(reg_data["email"], expected_user_data)
    LeadUpdate(api_timeout=API_TIMEOUT, api_url=API_URL)(user=user)


def test_success_validate_user_response() -> None:
    expected_id = 1
    actual_id = UserResponse.model_validate({"id": 1}).id
    assert actual_id == expected_id


def test_failed_validate_user_response() -> None:
    with pytest.raises(ValidationError) as exc:
        UserResponse.model_validate({"TEST": 1}).id
    assert exc.typename == "ValidationError"


@pytest.mark.django_db
def test_success_serialize_user(
    user: User,
    expected_serialized_user: dict[str, Any]
) -> None:
    actial_serialization = _serialize_user(user=user)
    assert actial_serialization == expected_serialized_user

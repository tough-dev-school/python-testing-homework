import pytest

from server.apps.identity.intrastructure.services.placeholder import (
    _serialize_user
)

pytestmark = [pytest.mark.django_db]


def test_serialize_user_non_empty_birthday(user):
    serialized = _serialize_user(user)
    assert serialized["name"] == user.first_name
    assert serialized["last_name"] == user.last_name
    assert isinstance(serialized["birthday"], str)
    assert len(serialized["birthday"]) > 0
    assert serialized["city_of_birth"] == user.address
    assert serialized["position"] == user.job_title
    assert serialized["email"] == user.email
    assert serialized["phone"] == user.phone


def test_serialize_user_empty_birthday(user):
    user.date_of_birth = None
    serialized = _serialize_user(user)
    assert serialized["birthday"] == ""

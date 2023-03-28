"""Test User model."""
import pytest
from django.db.utils import IntegrityError

from server.apps.identity.models import User

pytestmark = pytest.mark.django_db


def test_create_user(user_data) -> None:
    """Test creating a regular user."""
    user = User.objects.create_user(**user_data)
    user_data_filtered = {
        key: field_value
        for key, field_value in user_data.items()
        if key != 'password'
    }
    for field, field_value in user_data_filtered.items():
        assert getattr(user, field) == field_value
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser(user_data) -> None:
    """Test creating a superuser."""
    user = User.objects.create_superuser(**user_data)
    user_data_filtered = {
        key: field_value
        for key, field_value in user_data.items()
        if key != 'password'
    }
    for field, field_value in user_data_filtered.items():
        assert getattr(user, field) == field_value
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser


def test_user_email_uniqueness(user_data) -> None:
    """Test email uniqueness constraint."""
    User.objects.create_user(**user_data)

    user_data2 = user_data.copy()
    user_data2['email'] = user_data['email']

    with pytest.raises(IntegrityError, match='.*email.*'):
        User.objects.create_user(**user_data2)


def test_create_user_without_email(user_data) -> None:
    """Test creating a user without an email."""
    user_data['email'] = ''
    with pytest.raises(ValueError, match='.*email.*'):
        User.objects.create_user(**user_data)

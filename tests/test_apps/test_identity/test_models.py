"""Test User model."""
from datetime import date, timedelta

import pytest
from django.db.utils import IntegrityError
from mimesis import Address, Person

from server.apps.identity.models import User

person = Person()
address = Address()

pytestmark = pytest.mark.django_db

DAYS_IN_YEAR = 365


@pytest.fixture()
def user_data() -> dict[str, object]:
    """Generate random user data fixture."""
    age = person.age()
    birthdate = date.today() - timedelta(days=age * DAYS_IN_YEAR)

    return {
        'email': person.email(),
        'password': person.password(),
        'first_name': person.first_name(),
        'last_name': person.last_name(),
        'date_of_birth': birthdate,
        'address': address.address(),
        'job_title': person.occupation(),
        'phone': person.telephone(),
    }


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

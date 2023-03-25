from typing import Callable, TypedDict
from unittest.mock import patch

import faker
import pytest
from mixer.backend.django import mixer
from typing_extensions import TypeAlias

from server.apps.identity.models import User

fake = faker.Faker()


class UserCredentials(TypedDict):
    """User credentials for registration."""

    email: str
    password1: str
    password2: str


class UserData(TypedDict):
    """User data for registration."""

    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@pytest.fixture()
def user_credentials() -> UserCredentials:
    """Generate user credentials for registration."""
    password = fake.password()
    user_credentials = {
        'email': fake.email(),
        'password1': password,
        'password2': password,
    }
    return UserCredentials(
        **user_credentials,
    )


@pytest.fixture()
def user_data() -> UserData:
    """Generate user data for registration."""
    user_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': fake.date_of_birth(),
        'address': fake.address(),
        'job_title': fake.job(),
        'phone': fake.phone_number(),
    }
    return UserData(
        **user_data,
    )


UserAssertion: TypeAlias = Callable[[UserCredentials, UserData], None]


@pytest.fixture()
def assert_user_was_created() -> UserAssertion:
    """Assert that user was created with correct data."""

    def factory(user_credentials: UserCredentials, user_data: UserData) -> None:
        user = User.objects.get(email=user_credentials['email'])
        assert user.id
        assert user.check_password(user_credentials['password1'])
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_anonymous
        assert user.is_authenticated
        for field in user.REQUIRED_FIELDS:
            assert getattr(user, field) == user_data[field]

    return factory


@pytest.fixture()
def assert_user_update() -> UserAssertion:
    """Assert that user was updated with correct data."""
    def factory(user: User, user_data: UserData) -> None:
        user.refresh_from_db()
        for field in user_data.keys():
            assert getattr(user, field) == user_data[field]
    return factory


@pytest.fixture()
def user():
    """Create a user instance."""
    return mixer.blend(User, is_active=True)


@pytest.fixture()
def mock_authenticate():
    """Mock authenticate method."""
    with patch('server.apps.identity.models.User.check_password') as auth_mock:
        yield auth_mock

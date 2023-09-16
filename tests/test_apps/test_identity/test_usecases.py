import pytest

from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_create_user(user_factory):
    """Test user creation."""
    user = user_factory()

    assert user.is_active


@pytest.mark.django_db()
def test_create_new_user(user_factory, mock_lead_create):
    """Test create new user with lead"""
    user_create_new = container.instantiate(UserCreateNew)
    user = user_factory()

    user_create_new(user)

    user = User.objects.get(email=user.email)
    assert user.lead_id == int(mock_lead_create)

import pytest

from server.apps.identity.models import User

pytestmark = [
    pytest.mark.django_db,
]


def test_without_email():
    """Test create user via manager with incorrect email."""
    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(  # noqa: S106 not secure issue
            email='',
            password='SeCr3t',
        )

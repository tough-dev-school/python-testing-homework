import pytest

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_email_is_required(user_data_factory):
    with pytest.raises(ValueError):
        user_data = user_data_factory()
        user_data.pop('email')
        User.objects.create_user(None, 'a', **user_data)

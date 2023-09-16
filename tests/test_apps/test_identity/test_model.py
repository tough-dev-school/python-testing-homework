import pytest

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_manager_create_error():
    """If email is missing, error is called."""
    with pytest.raises(ValueError) as e_info:
        User.objects.create_user(
            email=None,
            password='',
            first_name='',
            last_name='',
            phone='',
        )
    assert e_info.value.args[0] == 'Users must have an email address'
